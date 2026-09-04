#!/usr/bin/env python3
"""Tests for schema evolution of datamodels that build on an upstream EDM.

Schema evolution (``OLD_DESCRIPTIONS``) and an upstream EDM (``UPSTREAM_EDM``)
used to be mutually exclusive in practice, because the code generator dropped
the upstream EDM when re-reading the schemas for comparison, and because the
old version PODs qualified upstream types with *this* datamodel's schema
version. Both are exercised here.
"""

import os
import shutil
import tempfile
import unittest

from podio_gen.podio_config_reader import PodioConfigReader
from podio_gen.cpp_generator import CPPClassGenerator

UPSTREAM_YAML = """
schema_version: 6
options:
  includeSubfolder: true
components:
  upstream::Vector3f:
    Members:
      - float x
      - float y
      - float z
datatypes:
  upstream::Hit:
    Description: "An upstream hit"
    Author: "podio"
    Members:
      - float energy // energy
"""

# The downstream datatype has a member whose type comes from the upstream EDM.
OLD_YAML = """
schema_version: 81000
options:
  includeSubfolder: true
  exposePODMembers: False
datatypes:
  downstream::Cluster:
    Description: "A downstream cluster"
    Author: "podio"
    Members:
      - upstream::Vector3f position // position
      - int oldName // to be renamed
"""

NEW_YAML = """
schema_version: 81100
options:
  includeSubfolder: true
  exposePODMembers: False
datatypes:
  downstream::Cluster:
    Description: "A downstream cluster"
    Author: "podio"
    Members:
      - upstream::Vector3f position // position
      - int newName // renamed
"""

EVOLUTION_YAML = """
migrations:
  downstream::Cluster:
    - from_version: 81000
      to_version: 81100
      rename_member: {from: oldName, to: newName}
"""


class UpstreamSchemaEvolutionTest(unittest.TestCase):
    """Code generation with both an upstream EDM and old schema descriptions"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.paths = {}
        for name, content in (
            ("upstream.yaml", UPSTREAM_YAML),
            ("old.yaml", OLD_YAML),
            ("new.yaml", NEW_YAML),
            ("evolution.yaml", EVOLUTION_YAML),
        ):
            path = os.path.join(self.tmpdir, name)
            with open(path, "w", encoding="utf-8") as yaml_file:
                yaml_file.write(content)
            self.paths[name] = path

        self.outdir = os.path.join(self.tmpdir, "out")
        # Creating the output directories is the responsibility of the caller
        # (podio_class_generator.py does the same)
        for sub_dir in ("src", "downstream"):
            os.makedirs(os.path.join(self.outdir, sub_dir), exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _generate(self):
        """Run the generator the same way podio_class_generator.py does"""
        upstream_edm = PodioConfigReader.read(self.paths["upstream.yaml"], package_name="upstream")
        generator = CPPClassGenerator(
            self.paths["new.yaml"],
            self.outdir,
            "downstream",
            io_handlers=["ROOT"],
            verbose=False,
            dryrun=False,
            upstream_edm=upstream_edm,
            old_descriptions=[self.paths["old.yaml"]],
            evolution_file=self.paths["evolution.yaml"],
        )
        generator.process()

    def test_generation_with_upstream_edm_succeeds(self):
        """The upstream EDM must be taken into account when re-reading the
        schemas for comparison, otherwise validation rejects upstream types."""
        try:
            self._generate()
        except Exception as exc:  # noqa: BLE001  pylint: disable=broad-except
            self.fail(f"Code generation with an upstream EDM and old schemas failed: {exc}")

    def test_old_version_pod_does_not_version_upstream_types(self):
        """Upstream types are versioned by the upstream EDM, so the old version
        PODs must refer to them unqualified rather than inventing a namespace
        such as ``upstream::v81000``."""
        self._generate()

        data_header = os.path.join(self.outdir, "downstream", "ClusterData.h")
        self.assertTrue(os.path.exists(data_header), f"{data_header} was not generated")
        with open(data_header, "r", encoding="utf-8") as header:
            contents = header.read()

        # The old version POD lives in a v81000 namespace ...
        self.assertIn("namespace v81000", contents)
        # ... but the upstream type must not be qualified with that version
        self.assertNotIn("upstream::v81000", contents)
        self.assertIn("::upstream::Vector3f position", contents)


if __name__ == "__main__":
    unittest.main()
