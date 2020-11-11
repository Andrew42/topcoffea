import coffea
import numpy as np
import copy
from modules.WCFit import WCFit

class HistEFT(coffea.hist.Hist):

  def __init__(self, label, wcnames, *axes, **kwargs):
    """ Initialize. Example:
          HistEFT("Events", ['c1', 'c2', 'c3'], hist.Cat("sample", "sample"), hist.Cat("cut", "cut"), hist.Bin("met", "MET (GeV)", 40, 0, 400))
    """
    if isinstance(wcnames, str) and ',' in wcnames: wcnames = wcnames.replace(' ', '').split(',')
    n = len(wcnames) if isinstance(wcnames, list) else wcnames
    self._wcnames = wcnames
    self._nwc = n
    self._ncoeffs = int(1+2*n+n*(n-1)/2)
    self.CreatePairs()

    super().__init__(label, *axes, **kwargs)

    self.EFTcoeffs = {}
    self.EFTerrs   = {}
    self.WCFit     = {}

  def CreatePairs(self):
    """ Create pairs... same as for WCFit class """
    self.idpairs  = []
    self.errpairs = []
    n = self._nwc
    for f in range(n+1):
      for i in range(f+1):
        self.idpairs.append((f,i))
        for j in range(len(self.idpairs)-1):
          self.errpairs.append((i,j))

  def GetErrCoeffs(self, coeffs):
    """ Get all the w*w coefficients """
    return [coeffs[p[0]]*coeffs[p[1]] if (p[1] == p[0]) else 2*(coeffs[p[0]]*coeffs[p[1]]) for p in self.errpairs]

  def copy(self, content=True):
    """ Copy """
    out = HistEFT(self._label, self._wcnames, *self._axes, dtype=self._dtype)
    if self._sumw2 is not None: out._sumw2 = {}
    if content:
        out._sumw = copy.deepcopy(self._sumw)
        out._sumw2 = copy.deepcopy(self._sumw2)
    out.EFTcoeffs = copy.deepcopy(self.EFTcoeffs)
    out.EFTerrs =  copy.deepcopy(self.EFTerrs)
    return out

  def identity(self):
    return self.copy(content=False)

  def clear(self):
    self._sumw = {}
    self._sumw2 = None
    self.EFTcoeffs = {}
    self.EFTerrs   = {}
    self.WCFit     = {}

  def GetNcoeffs(self):
    """ Number of coefficients """
    return self._ncoeffs

  def GetNcoeffsErr(self):
    """ Number of w*w coefficients """
    return int((self._ncoeffs+1)*(self._ncoeffs)/2)

  def GetSparseKeys(self, **values):
    """ Get tuple from values """
    return tuple(d.index(values[d.name]) for d in self.sparse_axes())

  def Fill(self, EFTcoefficients, **values):
    """ Fill histogram, incuding EFT fit coefficients """
    values_orig = values.copy()
    weight = values.pop("weight", None)

    sparse_key = tuple(d.index(values[d.name]) for d in self.sparse_axes())
    if sparse_key not in self.EFTcoeffs:
      self.EFTcoeffs[sparse_key] = []
      self.EFTerrs  [sparse_key] = []
      for i in range(self.GetNcoeffs()   ): self.EFTcoeffs[sparse_key].append(np.zeros(shape=self._dense_shape, dtype=self._dtype))
      for i in range(self.GetNcoeffsErr()): self.EFTerrs  [sparse_key].append(np.zeros(shape=self._dense_shape, dtype=self._dtype))

    errs = []
    iCoeff, iErr = 0,0
    if self.dense_dim() > 0:
      dense_indices = tuple(d.index(values[d.name]) for d in self._axes if isinstance(d, coffea.hist.hist_tools.DenseAxis))
      xy = np.atleast_1d(np.ravel_multi_index(dense_indices, self._dense_shape))
      if len(EFTcoefficients) > 0: 
        EFTcoefficients = EFTcoefficients.regular()
        errs = [self.GetErrCoeffs(x) for x in EFTcoefficients]
      for coef in np.transpose(EFTcoefficients):
        coef = coffea.util._ensure_flat(coef)
        self.EFTcoeffs[sparse_key][iCoeff][:] += np.bincount(xy, weights=coef, minlength=np.array(self._dense_shape).prod() ).reshape(self._dense_shape)
        iCoeff += 1
      
      # Calculate errs...
      for err in np.transpose(errs):
        self.EFTerrs[sparse_key][iErr][:] += np.bincount(xy, weights=err, minlength=np.array(self._dense_shape).prod() ).reshape(self._dense_shape)
        iErr+=1
    else:
      for coef in np.transpose(EFTcoefficients):
        self.EFTcoeffs[sparse_key][iCoeff] += np.sum(coef)
      # Calculate errs...
      for err in np.transpose(errs):
        self.EFTerrs[sparse_key][iErr][:] += np.sum(err)
    self.fill(**values_orig)

  #######################################################################################
  def SetWCFit(self, key=None):
    if key==None: 
      for key in list(self._sumw.keys())[-1:]: self.SetWCFit(key)
      return
    self.WCFit[key] = []
    bins = np.transpose(self.EFTcoeffs[key]) #np.array((self.EFTcoeffs[key])[:]).transpose()
    errs = np.array((self.EFTerrs  [key])[:]).transpose()
    ibin = 0
    for fitcoeff, fiterrs in zip(bins, errs):
      self.WCFit[key].append(WCFit(tag='%i'%ibin, names=self._wcnames, coeffs=fitcoeff, errors=fiterrs))
      #self.WCFit[key][-1].Dump()
      ibin+=1

  def add(self, other):
    """ Add another histogram into this one, in-place """
    #super().add(other)
    if not self.compatible(other):
      raise ValueError("Cannot add this histogram with histogram %r of dissimilar dimensions" % other)
    raxes = other.sparse_axes()

    def add_dict(left, right):
      for rkey in right.keys():
        lkey = tuple(self.axis(rax).index(rax[ridx]) for rax, ridx in zip(raxes, rkey))
        if lkey in left:
          left[lkey] += right[rkey]
        else:
          left[lkey] = copy.deepcopy(right[rkey])

    if self._sumw2 is None and other._sumw2 is None: pass
    elif self._sumw2 is None:
      self._init_sumw2()
      add_dict(self._sumw2, other._sumw2)
    elif other._sumw2 is None:
      add_dict(self._sumw2, other._sumw)
    else:
      add_dict(self._sumw2, other._sumw2)
    add_dict(self._sumw, other._sumw)
    add_dict(self.EFTcoeffs, other.EFTcoeffs)
    add_dict(self.EFTerrs, other.EFTerrs)
    return self

  def DumpFits(self, key=''):
   """ Display all the fit parameters for all bins """
   if key == '': 
     for k in self.EFTcoeffs.keys(): self.DumpFits(k)
     return
   for fit in (len(self.WCFit[key])):
     fit.Dump()

  def ScaleFits(self, SF, key=''):
   """ Scale all the fits by some amount """
   if key == '': 
     for k in self.EFTcoeffs.keys(): self.ScaleFits(SF, k)
     return
   for fit in self.WCFit[key]:
     fit.Scale(SF)  
 

  def __getitem__(self, keys):
    """ Extended from parent class """
    if not isinstance(keys, tuple): keys = (keys,)
    if len(keys) > self.dim():  raise IndexError("Too many indices for this histogram")
    elif len(keys) < self.dim():
      if Ellipsis in keys:
        idx = keys.index(Ellipsis)
        slices = (slice(None),) * (self.dim() - len(keys) + 1)
        keys = keys[:idx] + slices + keys[idx + 1:]
      else:
        slices = (slice(None),) * (self.dim() - len(keys))
        keys += slices
    sparse_idx, dense_idx, new_dims = [], [], []

    for s, ax in zip(keys, self._axes):
      if isinstance(ax, coffea.hist.hist_tools.SparseAxis):
        sparse_idx.append(ax._ireduce(s))
        new_dims.append(ax)
      else:
        islice = ax._ireduce(s)
        dense_idx.append(islice)
        new_dims.append(ax.reduced(islice))
    dense_idx = tuple(dense_idx)

    def dense_op(array):
      return np.block(coffea.hist.hist_tools.assemble_blocks(array, dense_idx))

    out = HistEFT(self._label, self._wcnames, *new_dims, dtype=self._dtype)
    if self._sumw2 is not None: out._init_sumw2()
    for sparse_key in self._sumw:
      if not all(k in idx for k, idx in zip(sparse_key, sparse_idx)): continue
      if sparse_key in out._sumw:
        out._sumw[sparse_key] += dense_op(self._sumw[sparse_key])
        if self._sumw2 is not None:
          out._sumw2[sparse_key] += dense_op(self._sumw2[sparse_key])
      else:
        out._sumw[sparse_key] = dense_op(self._sumw[sparse_key]).copy()
        if self._sumw2 is not None:
          out._sumw2[sparse_key] = dense_op(self._sumw2[sparse_key]).copy()
    for sparse_key in self.EFTcoeffs:
      if not all(k in idx for k, idx in zip(sparse_key, sparse_idx)): continue
      if sparse_key in out.EFTcoeffs:
        for i in range(len(out.EFTcoeffs[sparse_key])):
          out.EFTcoeffs[sparse_key][i] += dense_op(self.EFTcoeffs[sparse_key][i])
          out.EFTerrs  [sparse_key][i] += dense_op(self.EFTerrs  [sparse_key][i])
      else: 
        out.EFTcoeffs[sparse_key]=[]; out.EFTerrs[sparse_key]=[]; 
        for i in range(self.GetNcoeffs()   ): out.EFTcoeffs[sparse_key].append(np.zeros(shape=self._dense_shape, dtype=self._dtype))
        for i in range(self.GetNcoeffsErr()): out.EFTerrs  [sparse_key].append(np.zeros(shape=self._dense_shape, dtype=self._dtype))
        for i in range(len(self.EFTcoeffs[sparse_key])):
          out.EFTcoeffs[sparse_key][i] += dense_op(self.EFTcoeffs[sparse_key][i]).copy()
          out.EFTerrs  [sparse_key][i] += dense_op(self.EFTerrs  [sparse_key][i]).copy()
    return out

  def sum(self, *axes, **kwargs):
    """ Integrates out a set of axes, producing a new histogram 
        Project() and integrate() depends on sum() and are heritated """
    overflow = kwargs.pop('overflow', 'none')
    axes = [self.axis(ax) for ax in axes]
    reduced_dims = [ax for ax in self._axes if ax not in axes]
    out = HistEFT(self._label, self._wcnames, *reduced_dims, dtype=self._dtype)
    if self._sumw2 is not None: out._init_sumw2()

    sparse_drop = []
    dense_slice = [slice(None)] * self.dense_dim()
    dense_sum_dim = []
    for axis in axes:
      if isinstance(axis, coffea.hist.hist_tools.DenseAxis):
        idense = self._idense(axis)
        dense_sum_dim.append(idense)
        dense_slice[idense] = overflow_behavior(overflow)
      elif isinstance(axis, coffea.hist.hist_tools.SparseAxis):
        isparse = self._isparse(axis)
        sparse_drop.append(isparse)
    dense_slice = tuple(dense_slice)
    dense_sum_dim = tuple(dense_sum_dim)

    def dense_op(array):
      if len(dense_sum_dim) > 0:
        return np.sum(array[dense_slice], axis=dense_sum_dim)
      return array

    for key in self._sumw.keys():
      new_key = tuple(k for i, k in enumerate(key) if i not in sparse_drop)
      if new_key in out._sumw:
        out._sumw[new_key] += dense_op(self._sumw[key])
        if self._sumw2 is not None:
          out._sumw2[new_key] += dense_op(self._sumw2[key])
      else:
        out._sumw[new_key] = dense_op(self._sumw[key]).copy()
        if self._sumw2 is not None:
          out._sumw2[new_key] = dense_op(self._sumw2[key]).copy()

    for key in self.EFTcoeffs.keys():
      new_key = tuple(k for i, k in enumerate(key) if i not in sparse_drop)
      if new_key in out.EFTcoeffs:
        #out.EFTcoeffs[new_key] += dense_op(self.EFTcoeffs[key])
        #out.EFTerrs  [new_key] += dense_op(self.EFTerrs  [key])
        for i in range(len(self.EFTcoeffs[key])):
          out.EFTcoeffs[new_key][i] += dense_op(self.EFTcoeffs[key][i])
        for i in range(len(self.EFTerrs[key])):
          out.EFTerrs  [new_key][i] += dense_op(self.EFTerrs[key][i])
      else:
        out.EFTcoeffs[new_key] = []
        out.EFTerrs[new_key] = []
        for i in range(len(self.EFTcoeffs[key])):
          out.EFTcoeffs[new_key].append( dense_op(self.EFTcoeffs[key][i]).copy() )
        for i in range(len(self.EFTerrs[key])):
          out.EFTerrs  [new_key].append( dense_op(self.EFTerrs  [key][i]).copy() )
    return out

  def project(self, *axes, **kwargs):
    """ Project histogram onto a subset of its axes
         Same as in parent class """
    overflow = kwargs.pop('overflow', 'none')
    axes = [self.axis(ax) for ax in axes]
    toremove = [ax for ax in self.axes() if ax not in axes]
    return self.sum(*toremove, overflow=overflow)

  def integrate(self, axis_name, int_range=slice(None), overflow='none'):
    """ Integrates current histogram along one dimension
          Same as in parent class """
    axis = self.axis(axis_name)
    full_slice = tuple(slice(None) if ax != axis else int_range for ax in self._axes)
    if isinstance(int_range, coffea.hist.hist_tools.Interval):
      # Handle overflow intervals nicely
      if   int_range.nan()        : overflow = 'justnan'
      elif int_range.lo == -np.inf: overflow = 'under'
      elif int_range.hi ==  np.inf: overflow = 'over'
    return self[full_slice].sum(axis.name, overflow=overflow)  # slice may make new axis, use name

  def remove(self, bins, axis):
    """ Remove bins from a sparse axis
        Same as in parent class """
    axis = self.axis(axis)
    if not isinstance(axis, SparseAxis):
      raise NotImplementedError("Hist.remove() only supports removing items from a sparse axis.")
    bins = [axis.index(binid) for binid in bins]
    keep = [binid.name for binid in self.identifiers(axis) if binid not in bins]
    full_slice = tuple(slice(None) if ax != axis else keep for ax in self._axes)
    return self[full_slice]

  def Eval(self, WCPoint):
    """ Eval to a given WC point """
    if len(self.WCFit.keys()) == 0: self.SetWCFit()
    if not hasattr(self,'_sumw_orig'): 
      self._sumw_orig  = self._sumw.copy()
      self._sumw2_orig = self._sumw2.copy()
    for key in self.WCFit.keys():
      weights = np.array([wc.EvalPoint(     WCPoint) for wc in self.WCFit[key]])
      errors  = np.array([wc.EvalPointError(WCPoint) for wc in self.WCFit[key]])
      self._sumw [key] = self._sumw_orig [key]*weights
      self._sumw2[key] = self._sumw2_orig[key]*errors
      
    # group, rebin

