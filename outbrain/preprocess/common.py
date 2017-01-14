
from ..csvutil.reader import csv_file_group_iter_mutable


class MapStreamer(object):
    pass


class ReduceStreamer(object):
    """
    apply bunch of classes (aka mappers or reducers) processing a group of examples.
    """
    def __init__(self, reducers=None, group_field=None, infilename=None, outfilename=None,
                 separator=",", replace_header=("^", "_")):
        self._reducers = reducers
        self._examples_count = 0
        self._groups_count = 0
        self._group_field = group_field
        self._infilename = infilename
        self._outfilename = outfilename
        self._separator = separator
        self._replace_header = replace_header

        self._add_fields = []
        for reducer in reducers:
            self._add_fields.extend(reducer.add_fields)

    @property
    def add_fields(self):
        return self._add_fields

    def _write_batch_to_stream(self, batch, fields, outstream):
        for example in batch:
            #print len(example.keys())
            res = [str(getattr(example, field)) for field in fields]
            outstream.write("%s\n" % self._separator.join(res))

    def __call__(self):

        with open(self._infilename) as tmp:
            header = tmp.readline().strip()

        if self._replace_header:
            header = header.replace(self._replace_header[0], self._replace_header[1])

        new_header = "%s%s%s\n" % (header, self._separator,
                                 self._separator.join(self.add_fields))


        out_fields = new_header.strip().split(self._separator)

        with open(self._outfilename, "w") as outfile:
            outfile.write(new_header)

            with open(self._infilename) as infile:
                for group_key, examples_batch in csv_file_group_iter_mutable(
                        infile,
                        group_field=self._group_field
                        ):

                    self._examples_count += len(examples_batch)
                    self._groups_count += 1

                    for reducer in self._reducers:
                        print "processing mapreducer %s" % reducer.NAME
                        reducer(examples_batch)

                    self._write_batch_to_stream(examples_batch, out_fields,
                                                outfile)



def apply_mapreducers(infile, outfile, reducers, group_field, separator=","):

    streamer = ReduceStreamer(reducers=reducers, group_field=group_field,
                              infilename=infile, outfilename=outfile)

    streamer()









