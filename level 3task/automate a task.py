import os
import shutil
import datetime
import time
import logging
from pathlib import Path
import argparse
import csv

class FileOrganizer:
    """
    A class to organize files in a directory based on their extensions.
    Files are moved to categorized folders and a report is generated.
    """
    
    CATEGORIES = {
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
        'videos': ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm'],
        'audio': ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a'],
        'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
        'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.ts'],
        'data': ['.csv', '.json', '.xml', '.sql', '.db', '.sqlite', '.xlsx']
    }
    
    def __init__(self, source_dir=None, exclude_dirs=None, log_level=logging.INFO):
        """
        Initialize the FileOrganizer with source directory and logging setup.
        
        Args:
            source_dir (str): Directory to organize. Defaults to current directory.
            exclude_dirs (list): List of directory names to exclude.
            log_level: Logging level (e.g., logging.INFO, logging.DEBUG)
        """
        self.source_dir = source_dir if source_dir else os.getcwd()
        self.source_dir = os.path.abspath(self.source_dir)
        
        self.exclude_dirs = exclude_dirs if exclude_dirs else []
        
        self.exclude_dirs.extend(self.CATEGORIES.keys())
        
        self.exclude_dirs.append('reports')
        
        self.setup_logging(log_level)
        
        self.stats = {
            'total_files': 0,
            'organized_files': 0,
            'skipped_files': 0,
            'by_category': {category: 0 for category in self.CATEGORIES}
        }
    
    def setup_logging(self, log_level):
        """Configure logging for the file organizer."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        reports_dir = os.path.join(self.source_dir, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        log_file = os.path.join(reports_dir, f'file_organization_{timestamp}.log')
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"File organization started for directory: {self.source_dir}")
        self.logger.info(f"Log file will be saved to: {log_file}")
        
        self.reports_dir = reports_dir
        self.timestamp = timestamp
    
    def get_category(self, file_ext):
        """
        Determine category based on file extension.
        
        Args:
            file_ext (str): File extension including the dot (e.g., '.pdf')
            
        Returns:
            str: Category name or 'misc' if not found
        """
        file_ext = file_ext.lower()
        
        for category, extensions in self.CATEGORIES.items():
            if file_ext in extensions:
                return category
        
        return 'misc'
    
    def organize_files(self):
        """
        Main method to organize all files in the source directory.
        """
        self.logger.info("Starting file organization process...")
        start_time = time.time()
        
        for root, dirs, files in os.walk(self.source_dir, topdown=True):
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            
            for filename in files:
                self.stats['total_files'] += 1
                file_path = os.path.join(root, filename)
                
                if os.path.islink(file_path):
                    self.logger.debug(f"Skipping symbolic link: {file_path}")
                    self.stats['skipped_files'] += 1
                    continue
                
                _, file_ext = os.path.splitext(filename)
                if not file_ext:  
                    self.logger.debug(f"Skipping file without extension: {filename}")
                    self.stats['skipped_files'] += 1
                    continue
                
                category = self.get_category(file_ext)
                
                category_dir = os.path.join(self.source_dir, category)
                os.makedirs(category_dir, exist_ok=True)
                
                dest_path = os.path.join(category_dir, filename)
                
                if os.path.exists(dest_path):
                    name, ext = os.path.splitext(filename)
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_filename = f"{name}_{timestamp}{ext}"
                    dest_path = os.path.join(category_dir, new_filename)
                    self.logger.info(f"File already exists. Renaming to: {new_filename}")
                
                try:
                    shutil.move(file_path, dest_path)
                    self.logger.info(f"Moved: {filename} -> {category}/{os.path.basename(dest_path)}")
                    
                    self.stats['organized_files'] += 1
                    self.stats['by_category'][category] = self.stats['by_category'].get(category, 0) + 1
                    
                except Exception as e:
                    self.logger.error(f"Error moving {filename}: {str(e)}")
                    self.stats['skipped_files'] += 1
        
        elapsed_time = time.time() - start_time
        self.logger.info(f"File organization completed in {elapsed_time:.2f} seconds")
        
        self.generate_report()
    
    def generate_report(self):
        """
        Generate a summary report of the file organization process.
        """
        self.logger.info("Generating organization report...")
        
        csv_path = os.path.join(self.reports_dir, f'organization_report_{self.timestamp}.csv')
        
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            writer.writerow(['Report Type', 'Value'])
            
            writer.writerow(['Total Files Processed', self.stats['total_files']])
            writer.writerow(['Files Organized', self.stats['organized_files']])
            writer.writerow(['Files Skipped', self.stats['skipped_files']])
            
            writer.writerow(['', ''])
            writer.writerow(['Category', 'Count'])
            
            for category, count in self.stats['by_category'].items():
                if count > 0:  
                    writer.writerow([category, count])
        
        self.logger.info(f"Report saved to: {csv_path}")
        
        print("\n" + "="*50)
        print(f"FILE ORGANIZATION SUMMARY")
        print("="*50)
        print(f"Source Directory: {self.source_dir}")
        print(f"Total Files Processed: {self.stats['total_files']}")
        print(f"Files Organized: {self.stats['organized_files']}")
        print(f"Files Skipped: {self.stats['skipped_files']}")
        print("\nFiles by Category:")
        
        for category, count in self.stats['by_category'].items():
            if count > 0:
                print(f"  - {category}: {count}")
        
        print("\nDetailed log saved to:", os.path.join(self.reports_dir, f'file_organization_{self.timestamp}.log'))
        print("CSV report saved to:", csv_path)
        print("="*50 + "\n")


def main():
    parser = argparse.ArgumentParser(description='Organize files in a directory based on file types.')
    
    parser.add_argument('-d', '--directory', 
                        help='Directory to organize (default: current directory)',
                        default=None)
    
    parser.add_argument('-e', '--exclude', 
                        help='Directories to exclude (comma-separated)',
                        default='')
    
    parser.add_argument('-v', '--verbose', 
                        action='store_true',
                        help='Enable verbose output')
    
    args = parser.parse_args()
    
    log_level = logging.DEBUG if args.verbose else logging.INFO
    
    exclude_dirs = [d.strip() for d in args.exclude.split(',') if d.strip()]
    
    organizer = FileOrganizer(
        source_dir=args.directory,
        exclude_dirs=exclude_dirs,
        log_level=log_level
    )
    
    organizer.organize_files()


if __name__ == "__main__":
    main()