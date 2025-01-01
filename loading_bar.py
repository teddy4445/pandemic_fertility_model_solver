import os
import sys
import time


class LoadingBar:

    def __init__(self,
                 length: int = 25):
        self.bars = {}
        self.start_times = {}
        self.length = length

    def register(self, name, total):
        self.bars[name] = {'iteration': 0, 'total': total}
        self.start_times[name] = time.time()

    def remove(self, name):
        if name in self.bars:
            del self.bars[name]
            del self.start_times[name]

    def update(self, name, iteration):
        if name in self.bars:
            self.bars[name]['iteration'] = iteration

    def refresh(self):
        # Move the cursor up by the number of bars to overwrite the previous output
        sys.stdout.write("\033[F" * len(self.bars))

        # Clear all the lines
        for _ in range(len(self.bars)):
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[F")

        # Print all bars
        text_to_print = ""
        for name, data in self.bars.items():
            text_to_print += self._print_bar(name, data['iteration'], data['total'], self.start_times[name])
        text_to_print += "\n"
        sys.stdout.write(text_to_print)
        sys.stdout.flush()

    def _print_bar(self, name, iteration, total, start_time):
        elapsed_time = time.time() - start_time
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(self.length * iteration // total)
        bar = '#' * filled_length + '-' * (self.length - filled_length)

        if iteration == total:
            return f'[{bar}] 100% Complete | Elapsed Time: {elapsed_time:.1f}s\n'
        else:
            estimated_total_time = elapsed_time * (total / iteration) if iteration > 0 else 0
            remaining_time = estimated_total_time - elapsed_time
            estimated_time_str = f"{remaining_time:.1f}s remaining" if iteration > 0 else "Calculating time..."
            return f'{name:<12}: [{bar}] {percent}% Complete | Elapsed Time: {elapsed_time:.1f}s | {estimated_time_str}\n'
