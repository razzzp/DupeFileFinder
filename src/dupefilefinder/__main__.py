
import argparse
import pathlib
from typing import List, Dict

class DupeFileFinder:
   def __init__(self) -> None:
      self._seen_paths: Dict[str, List[pathlib.Path]] = dict()

   def _search_dupes_recurs(self, dir_path: pathlib.Path):
      for child in dir_path.iterdir():
         if child.is_dir():
            # search dir
            self.search_dupes(child)
         else:
            paths_seen = self._seen_paths.get(child.name)
            if paths_seen:
               # append to list of seen paths
               paths_seen.append(child)
            else:
               # initialize list of seen paths
               self._seen_paths[child.name] = [child,]
   
   def search_dupes(self, dir_path: pathlib.Path) -> Dict[str, List[pathlib.Path]]:
      self._search_dupes_recurs(dir_path)
      return self._seen_paths

def main():
   parser = argparse.ArgumentParser(
      prog='Dupe File Finder',
      description='Find duplicate file names in a folder recursively.'
      )
   parser.add_argument('folder_path')
   args = parser.parse_args()

   # print(args.folder_path)
   folder_path = pathlib.Path(args.folder_path)
   if not folder_path.exists():
      print("Path '{}' does not exist".format(folder_path))
      exit(1)

   folder_path = folder_path.absolute()
   if not folder_path.is_dir():
      print("Path '{}' is not a directory".format(folder_path))
      exit(1)
   
   print("Searching '{}' for duplicate files...".format(folder_path))

   dupes = DupeFileFinder().search_dupes(folder_path)

   for dupe in dupes.items():
      if len(dupe[1]) > 1:
         print("\nDupes found for '{}':".format(dupe[0]))
         for path in dupe[1]:
            print("{}".format(path.absolute()))

if __name__ == '__main__':
   main()