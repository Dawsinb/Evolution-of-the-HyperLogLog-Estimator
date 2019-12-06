import statistics

#test formatter
def printTest(label, expected, actual, print_all):
  #print header
  print('*'*50)
  print('{s:{c}^{n}}'.format(s=f' {label} ', n=50, c='*'))
  print('*'*50)
  print()

  #print results
  print('{s:{c}^{n}}'.format(s=' Expected result ', n=50, c='-'))
  print(expected)
  if print_all:
    print('{s:{c}^{n}}'.format(s=' Actual results ', n=50, c='-'))
    print("\n".join("{0:.0f}".format(x) for x in actual))
  print('{s:{c}^{n}}'.format(s=' Mean result ', n=50, c='-'))
  print("{0:.0f}".format(statistics.mean(actual)))
  print()
  
  #print statistics
  print('{s:{c}^{n}}'.format(s=' Difference ', n=50, c='-'))
  print("{0:.0f}".format(abs(expected - statistics.mean(actual))))
  print('{s:{c}^{n}}'.format(s=' Percent Error ', n=50, c='-'))
  print("{0:.2%}".format(abs(expected - statistics.mean(actual)) / expected))
  print('{s:{c}^{n}}'.format(s=' Standard Deviation ', n=50, c='-'))
  print("{0:.0f}".format(statistics.pstdev(actual)))
  print()
  print()