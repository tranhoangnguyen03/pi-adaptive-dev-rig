# Task: make the export safer

Work in this repository. The export script writes its output file
directly — if it dies halfway we're left with a half-written file that
downstream jobs happily pick up. Make the export safer.
