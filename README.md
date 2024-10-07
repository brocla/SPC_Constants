# Calculate SPC constants from scratch. No values taken from a table.

## The advantages are:
- available for any sample size.
- The sigma limits are adjustable to values other than 3 sigma.
- More decimal places than commonly available in tables.
- Comfort in knowing whence come these constants.


## Intended Audience
- Developers of SPC software
- Supply Chain professionals
- Process Engineers


## USAGE
```
>>> from spc_constants import SPC_Constants
>>> const = SPC_Constants(2, z=3)
>>> const.A2
1.8799712059732498
>>> const.D3
0
>>> const.D4
3.266531919339083
```


## GLOSSARY
```
Constant   Description
--------   -----------------------------------------------------------------
n          sample size
z          multiplier of sigma limits. The default is a +/- 3 sigma limit.
c4         unbiased estimator of the population standard deviation
c5         unbiased estimator for the standard deviation of the moving range
d2         unbiased estimator of the sample standard deviation
d3         unbiased estimator of the standard deviation of the range
A          X̄ limits based on standard sigma (rare). Pairs with <D1 and D2> or <B5 and B6>.
A2         X̄ limits based on calculated R-bar. Pairs with D3 and D4. (Common)
A3         X̄ limits based on calculated s-bar. Pairs with B3 and B4.
B3         LCL on s chart, given s-bar
B4         UCL on s chart, given s-bar
B5         LCL on s chart, given standard sigma 
B6         UCL on s chart, given standard sigma
D1         LCL on R chart when Standards given for sigma (rare). 
D2         UCL on R chart when Standards given for sigma (rare)
D3         LCL on R Chart. No standard given. Data used to estimate sigma. (common)
D4         UCL on R Chart. No standard given. Data used to estimate sigma. (common)
E2         I-MR Chart
E3         I-Ms Chart
```




## Sample (n=2, z=3.0)
```
     n  z     d2        d3        c4        A2        A3        B3        B4        D3        D4      
     2  3.00  1.128379  0.852502  0.797885  1.879971  2.658681  0.000000  3.266532  0.000000  3.266532
     3  3.00  1.692569  0.888368  0.886227  1.023327  1.954410  0.000000  2.568170  0.000000  2.574591
     4  3.00  2.058751  0.879808  0.921318  0.728597  1.628103  0.000000  2.266047  0.000000  2.282052
     5  3.00  2.325929  0.864082  0.939986  0.576819  1.427299  0.000000  2.088998  0.000000  2.114499

     6  3.00  2.534413  0.848040  0.951533  0.483246  1.287128  0.030363  1.969637  0.000000  2.003830
     7  3.00  2.704357  0.833205  0.959369  0.419284  1.181916  0.117685  1.882315  0.075708  1.924292
     8  3.00  2.847201  0.819831  0.965030  0.372527  1.099095  0.185090  1.814910  0.136171  1.863829
     9  3.00  2.970026  0.807834  0.969311  0.336697  1.031661  0.239133  1.760867  0.184013  1.815987
    10  3.00  3.077505  0.797051  0.972659  0.308264  0.975350  0.283706  1.716294  0.223023  1.776977

    11  3.00  3.172873  0.787315  0.975350  0.285084  0.927394  0.321280  1.678720  0.255582  1.744418
    12  3.00  3.258455  0.778478  0.977559  0.265778  0.885906  0.353512  1.646488  0.283269  1.716731
    13  3.00  3.335980  0.770416  0.979406  0.249417  0.849546  0.381556  1.618444  0.307176  1.692824
    14  3.00  3.406763  0.763023  0.980971  0.235351  0.817336  0.406245  1.593755  0.328081  1.671919
    15  3.00  3.471827  0.756211  0.982316  0.223109  0.788541  0.428200  1.571800  0.346559  1.653441
```

