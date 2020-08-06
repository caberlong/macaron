import sys                                                                                          
                                                                                                    
from model.vocabulary import Vocabulary
                                                                                                    
def main(argv):                                                                                     
  root_dir = '/Users/longchb/Documents/GitHub/macaron/data/store/yahoo_quote/example'               
  Vocabulary(root_dir).computeVocabs()

  
if __name__ == '__main__':                                                                          
  main(sys.argv) 
