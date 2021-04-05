from distutils.core import setup
setup(
  name = 'analyst_recommendation_performance',        
  packages = ['analyst_recommendation_performance'],   
  version = '1.0',      
  license='MIT',        
  description = 'Get the performance of analysts stock recommendation',  
  long_description= 'view docs at https://github.com/dbondi/analyst_recommendation_performance',
  author = 'Daniel Bondi',             
  author_email = 'dbondi@wisc.edu', 
  url = 'https://github.com/dbondi/analyst_recommendation_performance',  
  download_url = 'https://github.com/dbondi/analyst_recommendation_performance/archive/refs/tags/v1.0.tar.gz',    
  keywords = ['STOCKS', 'ANALYSTS', 'PYTHON', 'RECOMMENDATIONS','TICKERS'],  
  install_requires=[          
          'dateutil.relativedelta',
          'matplotlib.ticker',
          'matplotlib.pyplot',
          'matplotlib.patches',
          'matplotlib.scale',
          'yfinance'
          'numpy',
          'pandas'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',   
    'Intended Audience :: Developers',   
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',    
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)