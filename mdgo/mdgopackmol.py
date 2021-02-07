import subprocess
import os


class PackmolWrapper:
    def __init__(self, path, structures, numbers, box, tolerance=None,
                 seed=None, inputfile='packmol.inp', outputfile='output.xyz'):
        self.path = path
        self.input = os.path.join(self.path, inputfile)
        self.output = os.path.join(self.path, outputfile)
        self.screen = os.path.join(self.path, 'packmol.stdout')
        self.structures = structures
        self.numbers = numbers
        self.box = box
        if tolerance is None:
            self.tolerance = 2.0
        else:
            self.tolerance = tolerance
        if seed is None:
            self.seed = 123
        else:
            self.seed = seed

    def run_packmol(self):
        """Run and check that Packmol worked correctly"""
        try:
            p = subprocess.run('packmol < {}'.format(self.input),
                               check=True,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise ValueError("Packmol failed with errorcode {}"
                             " and stderr: {}".format(e.returncode, e.stderr))
        else:
            with open(self.screen, 'w') as out:
                out.write(p.stdout.decode())

    def make_packmol_input(self):
        """Make a Packmol usable input file"""

        with open(self.input, 'w') as out:
            out.write("# " + ' + '.join(self.numbers[structure["name"]] + " "
                                        + structure["name"] for structure
                                        in self.structures) + "\n")
            out.write("# Packmol input generated by mdgo.")
            out.write('seed {}\n'.format(self.seed))
            out.write('tolerance {}\n\n'.format(self.tolerance))
            out.write('filetype xyz\n\n')

            for structure in self.structures:
                out.write("structure {}\n".format(structure["file"]))
                out.write("  number {}\n".format(
                    self.numbers[structure["name"]]))
                out.write("  inside box {}\n".format(
                    " ".join(str(i) for i in self.box)))
                out.write("end structure\n\n")
            out.write('output {}\n\n'.format(self.output))


def main():
    structures = [{"name": "EMC",
                   "file": "/Users/th/Downloads/test_selenium/EMC.lmp.xyz"}]
    pw = PackmolWrapper("/Users/th/Downloads/test_selenium/", structures,
                        {"EMC": '2'}, [0., 0., 0., 10., 10., 10.])
    pw.make_packmol_input()
    pw.run_packmol()


if __name__ == "__main__":
    main()
