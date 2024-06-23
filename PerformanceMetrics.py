import time

class PerformanceMetrics:
    def __init__(self):
        self.tracking_data = {}
    
    def start_tracking(self, process_name):
        if process_name in self.tracking_data:
            print(f"Warning: Process '{process_name}' is already being tracked.")
        self.tracking_data[process_name] = {'start_time': time.time(), 'end_time': None}

    def end_tracking(self, process_name):
        if process_name not in self.tracking_data:
            print(f"Error: Process '{process_name}' was not started.")
            return
        if self.tracking_data[process_name]['end_time'] is not None:
            print(f"Warning: Process '{process_name}' has already ended.")
            return
        self.tracking_data[process_name]['end_time'] = time.time()
        self._print_duration(process_name)

    def _print_duration(self, process_name):
        start_time = self.tracking_data[process_name]['start_time']
        end_time = self.tracking_data[process_name]['end_time']
        if start_time and end_time:
            duration = end_time - start_time
            print(f"Process '{process_name}' ran for {duration:.4f} seconds.")
        else:
            print(f"Could not calculate duration for process '{process_name}'.")

    def get_duration(self, process_name):
        if process_name not in self.tracking_data:
            print(f"Error: Process '{process_name}' does not exist.")
            return None
        if self.tracking_data[process_name]['end_time'] is None:
            print(f"Warning: Process '{process_name}' has not ended yet.")
            return None
        return self.tracking_data[process_name]['end_time'] - self.tracking_data[process_name]['start_time']
