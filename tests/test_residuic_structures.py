from unittest import TestCase
import unittest.mock
from molecupy.structures import ResiduicStructure, Residue, AtomicStructure, Atom
from molecupy import NoResiduesError, DuplicateResiduesError

class ResiduicStructureTest(TestCase):

    def setUp(self):
        self.residues = [unittest.mock.Mock(spec=Residue) for _ in range(10)]
        for index, residue in enumerate(self.residues):
            residue.residue_id.return_value = index + 1



class ResiduicStructureCreationTests(ResiduicStructureTest):

    def test_can_create_residuic_structure(self):
        residuic_structure = ResiduicStructure(*self.residues)
        self.assertIsInstance(residuic_structure, AtomicStructure)
        self.assertEqual(residuic_structure._residues, set(self.residues))


    def test_can_only_create_residuic_structure_with_residues(self):
        with self.assertRaises(TypeError):
            ResiduicStructure("Atom1", "Atom2")


    def test_cannot_make_empty_residuic_structure(self):
        with self.assertRaises(NoResiduesError):
            ResiduicStructure()


    def test_cannot_have_duplicate_residue_ids_in_residuic_structure(self):
        self.residues[-1].residue_id.return_value = 9
        with self.assertRaises(DuplicateResiduesError):
            ResiduicStructure(*self.residues)


    def test_residuic_structure_repr(self):
        residuic_structure = ResiduicStructure(*self.residues)
        self.assertEqual(str(residuic_structure), "<ResiduicStructure (10 residues)>")



class ResiduicStructurePropertyTests(ResiduicStructureTest):

    def test_can_get_residues(self):
        residuic_structure = ResiduicStructure(*self.residues)
        self.assertEqual(residuic_structure.residues(), set(self.residues))


    def test_residuic_structure_residues_is_read_only(self):
        residue11 = unittest.mock.Mock(spec=Residue)
        residuic_structure = ResiduicStructure(*self.residues)
        self.assertEqual(len(residuic_structure.residues()), 10)
        residuic_structure.residues().add(residue11)
        self.assertEqual(len(residuic_structure.residues()), 10)


    def test_can_exclude_missing_residues(self):
        for residue in self.residues:
            residue.is_missing.return_value = False
        self.residues[6].is_missing.return_value = True
        residuic_structure = ResiduicStructure(*self.residues)
        self.assertEqual(
         len(residuic_structure.residues(include_missing=False)),
         9
        )
        self.assertNotIn(
         self.residues[6],
         residuic_structure.residues(include_missing=False)
        )


    def test_can_add_residue(self):
        residue11 = unittest.mock.Mock(spec=Residue)
        residuic_structure = ResiduicStructure(*self.residues)
        residuic_structure.add_residue(residue11)
        self.assertEqual(len(residuic_structure.residues()), 11)
        self.assertIn(residue11, residuic_structure.residues())


    def test_can_only_add_residues(self):
        residuic_structure = ResiduicStructure(*self.residues)
        with self.assertRaises(TypeError):
            residuic_structure.add_residue("atom21")


    def test_can_only_add_residues_if_id_is_unique(self):
        residuic_structure = ResiduicStructure(*self.residues[:-1])
        self.residues[-1].residue_id.return_value = 9
        with self.assertRaises(DuplicateResiduesError):
            residuic_structure.add_residue(self.residues[-1])


    def test_can_remove_residues(self):
        residuic_structure = ResiduicStructure(*self.residues)
        residuic_structure.remove_residue(self.residues[5])
        self.assertEqual(len(residuic_structure.residues()), 9)
        self.assertNotIn(self.residues[5], residuic_structure.residues())


    def test_can_get_atoms(self):
        atoms = [unittest.mock.Mock(spec=Atom) for _ in range(10)]
        for index, residue in enumerate(self.residues):
            residue.atoms.return_value = set([atoms[index]])
        residuic_structure = ResiduicStructure(*self.residues)
        self.assertEqual(residuic_structure._atoms, set(atoms))
        self.assertEqual(residuic_structure.atoms(), set(atoms))



class ResidueRetrievalTests(ResiduicStructureTest):

    def setUp(self):
        ResiduicStructureTest.setUp(self)
        for index, residue in enumerate(self.residues):
            residue.residue_id.return_value = "A%i" % (index + 1)
            residue.residue_name.return_value = "MET" if index % 2 else "TYR"
            residue.is_missing.return_value = False if index <= 5 else True
        self.residuic_structure = ResiduicStructure(*self.residues)


    def test_can_get_residue_by_id(self):
        self.assertIs(self.residuic_structure.get_residue_by_id("A1"), self.residues[0])
        self.assertIs(self.residuic_structure.get_residue_by_id("A3"), self.residues[2])
        self.assertIs(self.residuic_structure.get_residue_by_id("A9"), self.residues[8])
        self.assertIs(self.residuic_structure.get_residue_by_id("B76G"), None)


    def test_can_only_search_by_string_id(self):
        with self.assertRaises(TypeError):
            self.residuic_structure.get_residue_by_id(98)


    def test_can_get_residues_by_name(self):
        self.assertEqual(
         self.residuic_structure.get_residues_by_name("TYR"),
         set(self.residues[::2])
        )


    def test_can_get_present_residues_by_name(self):
        self.assertEqual(
         self.residuic_structure.get_residues_by_name("TYR", include_missing=False),
         set(self.residues[::2][:-2])
        )


    def test_failed_name_search_returns_empty_set(self):
        self.assertEqual(
         self.residuic_structure.get_residues_by_name("FX"),
         set()
        )


    def test_can_get_single_residue_by_name(self):
        self.assertIn(
         self.residuic_structure.get_residue_by_name("TYR"),
         set(self.residues[::2])
        )


    def test_can_get_single_residue_by_name_present_only(self):
        self.assertIn(
         self.residuic_structure.get_residue_by_name("TYR", include_missing=False),
         set(self.residues[::2][:-2])
        )


    def test_failed_single_name_search_returns_none(self):
        self.assertEqual(
         self.residuic_structure.get_residue_by_name("FX"),
         None
        )


    def test_can_only_search_by_string_name(self):
        with self.assertRaises(TypeError):
            self.residuic_structure.get_residues_by_name(None)
        with self.assertRaises(TypeError):
            self.residuic_structure.get_residue_by_name(None)
