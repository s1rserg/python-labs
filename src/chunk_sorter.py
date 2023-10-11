import mmap
import os


class ChunkSorter:
    def __init__(self, input_file, output_files):
        self.input_file = input_file
        self.output_files = output_files

    def sort_chunks(self):
        # вхідний файл ділиться на 10 блоків, кожен блок сортується і ділиться на 10 частин. у файл блоки записуються по
        # цим частинам. після запису кожної, перевіряється чи розмір не перевищив допустимого. виходить швидко і більш
        # менш рівні за розміром файли
        with open(self.input_file, 'r') as f:
            if os.stat(self.input_file).st_size != 0:
                mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            else:
                raise ValueError(f"Cannot memory map an empty input file")
            file_size = os.path.getsize(self.input_file)
            chunk_size = file_size // 10
            part_size = 10
            max_output_file_size = file_size // len(self.output_files)
            if chunk_size == 0:
                chunk = mmapped_file[0:len(mmapped_file)]
                lines = chunk.decode().splitlines()
                non_empty_lines = [line for line in lines if line]
                sorted_chunk = sorted(non_empty_lines, key=int)
                with open(self.output_files[0], 'a') as f_out:
                    f_out.write('\n'.join(sorted_chunk))
                    f_out.write('\n')
                return
            for i in range(0, file_size, chunk_size):
                chunk = mmapped_file[i:i + chunk_size]
                lines = chunk.decode().splitlines()
                non_empty_lines = [line for line in lines if line]
                sorted_chunk = sorted(non_empty_lines, key=int)
                if len(sorted_chunk) // part_size != 0:
                    chunk_parts = [sorted_chunk[j:j + len(sorted_chunk) // part_size] for j in
                                   range(0, len(sorted_chunk),
                                         len(sorted_chunk) // part_size)]
                else:
                    chunk_parts = sorted_chunk

                for chunk_part in chunk_parts:
                    for output_file in self.output_files:
                        if os.path.getsize(output_file) + max_output_file_size * (
                                1 / part_size ** 2) < max_output_file_size:
                            with open(output_file, 'a') as f_out:
                                f_out.write('\n'.join(chunk_part))
                                f_out.write('\n')
                            break
