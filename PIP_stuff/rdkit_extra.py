from rdkit import Chem
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem import Draw
from rdkit.Chem import rdFMCS
from rdkit.Chem import rdRascalMCES
import nispo
from pyopsin import PyOpsin


# To do:
# check if the loigc is right and validate
# check about a cleanup step -> maybe should be seperate function
# there must be a way to chech ionic forms
# the inchi is likely less accurate at checking the things as it must be made to smiles first?????
# string comparisons okay as comparisons???
# any mol to string conversion has some issues with the natural way that rdkit sanitizes and cleans molecules
# there is a smilesToMOL parameters forstrict parsing sanitizing and for removing H which is maybe nice for checking if same or not
# check if rdFMCS is a viable way to get if molecules are identical -> do not think so it seems that the stereochemistry is lost
# cite visual logic from the rdkit cookbook??
# implement smarts
# johnson similarity does not reliably distinguish between stereoisomers
# rename is same compound and is same mol

class compound_comparitor:
#////////////////////////////////////////////////////////////////////////input type dectector and agnostic input RDkit mol returner and general comparitors
    # detect if input was a smiles, inchi, iupac, rdkitMol
    def detect_input_type(self,input_value) -> str:
        if not input_value:
            raise ValueError('Cannot type empty value')
        if isinstance(input_value,str):
            if not input_value.strip():
                raise ValueError('Input value cannot be an empty string')
            input_value = input_value.strip()
            #check smiles
            mol = Chem.MolFromSmiles(input_value)
            if mol:
                return 'SMILES'
            mol = Chem.MolFromInchi(input_value)
            if mol:
                return 'InChi'
            try:
                opsin = PyOpsin()
                smiles = opsin.to_smiles_single(input_value)
                mol = Chem.MolFromSmiles(smiles)
                if mol:
                    return 'Iupac'
                else:
                    return 'unkown'
            except:
                return 'unknown'
        else:
            if isinstance(input_value, Chem.Mol):
                return 'RDKit Mol'
            else:
                return 'unknown'            

    def make_mol(self,input_value) -> Chem.Mol:
        if not input_value:
            raise ValueError('Input cannot be empty')

        value_type = self.detect_input_type(input_value)
        match value_type:
            case 'SMILES':
                input_value = input_value.strip()
                mol = Chem.MolFromSmiles(input_value)
                if mol:
                    return mol
                else:
                    raise Exception('Could not make mol from SMILES')
            case 'InChi':
                input_value = input_value.strip()
                mol = Chem.MolFromInchi(input_value)
                if mol:
                    return mol
                else:
                    raise Exception('Could not make mol from InChi')
            case 'Iupac':
                input_value = input_value.strip()
                opsin = PyOpsin()
                smiles = opsin.to_smiles_single(input_value)
                mol = Chem.MolFromSmiles(smiles)
                if mol:
                    return mol
                else:
                    raise Exception('Could not make mol from Iuapc')               
            case 'RDKit Mol':
                return input_value
            case 'unknown':
                raise Exception('Unknown type could not make mol')

    def is_same_string(self,string1:str, string2:str) -> bool:
        if not string1.strip() and not string2.strip():
            Exception('Empty strings cannot be compared')
        string1 = string1.strip()
        string2 = string2.strip()
        if string1 == string2:
            return True
        else:
            return False

    def is_same_mol(self, mol1: Chem.Mol, mol2: Chem.Mol) -> bool:
        smiles1 = Chem.MolToSmiles(mol1, canonical=True,isomericSmiles=True)
        smiles2 = Chem.MolToSmiles(mol2, canonical=True,isomericSmiles=True)

        if smiles1 == smiles2:
            return True
        else:
            False

    def are_stereoisomers(self, mol1: Chem.Mol, mol2: Chem.Mol) -> bool:
        non_isomeric_smile1 = Chem.MolToSmiles(mol1,isomericSmiles=False, canonical=True)
        non_isomeric_smile2 = Chem.MolToSmiles(mol2,isomericSmiles=False, canonical=True)

        if non_isomeric_smile1 == non_isomeric_smile2:
            return True
        else:
            return False

    def are_tautomers(self, mol1: Chem.Mol, mol2: Chem.Mol) -> bool:
        TautomerEnumerator = rdMolStandardize.TautomerEnumerator()
        tautomer1 = TautomerEnumerator.Canonicalize(mol1)
        tautomer2 = TautomerEnumerator.Canonicalize(mol2)

        tautomer_smiles1 = Chem.MolToSmiles(tautomer1)
        tautomer_smiles2 = Chem.MolToSmiles(tautomer2)

        if tautomer_smiles1 == tautomer_smiles2:
            return True
        else:
            return False        
                
#//////////////////////////////////////////////////////////////////////////compound cleaners ie detect multiple fragments and such
    def smiles_can_convert_to_mol(smiles:str,return_mol:bool)-> bool|bool,Chem.Mol:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            if not return_mol:
                return False
            else:
                return False, None
        if return_mol:
            return True,mol
        else:
            return False

    def smiles_santized_by_conversion(self,smiles):
        convertable, mol = self.smiles_can_convert_to_mol(smiles,return_mol=True):
        if convertable:
            new_smiles = Chem.MolToSmiles(mol)
            if smiles == new_smiles:
                return False
            else:
                return True
        else:
            raise Exception('Smiles cannot be converted to mol')
    
    def contains_metals(mol: Chem.Mol,list_metals: bool) -> bool|bool,set:
        metals = {
                'Li', 'Be','Na', 'Mg', 'Al','K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni',
                'Cu', 'Zn','Ga','Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd','Ag', 'Cd',
                'In', 'Sn','Cs', 'Ba','La', 'Ce','Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy','Ho', 
                'Er', 'Tm','Yb', 'Lu', 'Hf', 'Ta','W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg','Tl', 'Pb', 
                'Bi', 'Po','Fr', 'Ra','Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf','Es', 
                'Fm','Md', 'No', 'Lr','Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn','Nh', 'Fl', 'Mc', 'Lv'}

        mol_metals = set()
        for atom in mol.GetAtoms():
            if atom.GetSymbol() in metals and not list_metals:
                return True
            elif atom.GetSymbol() in metals and list_metals:
                mol_metals.add(atom.getSymbol)
        
        if not mol_metals and not list_metals:
            return False
        elif not mol_metals and list_metals:
            return False, mol_metals
        else:
            return True, mol_metals

    def multiple_fragments(mol: Chem.Mol) -> bool:
        fragments = Chem.GetMolFrags(mol,asMols=True)
        if fragments:
            return True
        else:
            return False
            
    def check_smiles(self,smiles: str)-> str:
        msg = ''
        # check smiles convertability
        convertable, mol = self.smiles_can_convert_to_mol(smiles,return_mol=True)
        if not convertable:
            msg = 'Cannot convert smiles to mol'
        # check if mol contains metals
        has_metals, metals = self.contains_metals(mol,list_metals=True)
        if has_metals:
            msg_metals = ''
            msg = msg + 'The following metals are found in the SMILES: ' + ', '.join(msg_metals) 
        # check if multiple fragments
        if self.multiple_fragments(mol):
            msg = msg + '\n' + 'SMILES contain multiple fragments'
        
#/////////////////////////////////////////////////////////////////////////smiles comparitor
    def compare_smiles(self,smile1:str, smile2:str) -> str:
        if not smile1.strip() and not smile2.strip():
            Exception('Empty smiles cannot be compared')
        smile1 = smile1.strip()
        smile2 = smile2.strip()
        #checks if input SMILE strings are identical 
        if self.is_same_string(smile1,smile2):
            return 'Input SMILES are the same'

        #convert SMILES to Mol
        mol1 = Chem.MolFromSmiles(smile1)
        mol2 = Chem.MolFromSmiles(smile2)
        #check if SMILES refer to the same compound (compound identical but has different smiles notations)
        if self.is_same_mol(mol1,mol2):
            return 'Input SMILES refer to the same compound'

        #check if compounds are stereoisomers of each other
        if self.are_stereoisomers(mol1,mol2):
            return 'Input SMILES are stereoisomers'

        #check if compounds are tautomers of each other
        if self.are_tautomers(mol1,mol2):
            return 'Input smiles are tautomers'

        return 'SMILES refer to different compounds'
#/////////////////////////////////////////////////////////////////////////inchi comparitor
    def compare_inchi(self,inchi1:str, inchi2:str) -> str:
        if not inchi1.strip() and not inchi2.strip():
            Exception('Empty smiles cannot be compared')
        inchi1 = inchi1.strip()
        inchi2 = inchi2.strip()
        #checks if input inchi strings are identical 
        if self.is_same_string(inchi1,inchi2):
            return 'Input SMILES are the same'

        #convert inchi to Mol
        mol1 = Chem.MolFromInchi(inchi1)
        mol2 = Chem.MolFromInchi(inchi2)
        #check if inchi refer to the same compound (compound identical but has different smiles notations)
        if self.is_same_mol(mol1,mol2):
            return 'Input InChis refer to the same compound'

        #check if compounds are stereoisomers of each other
        if self.are_stereoisomers(mol1,mol2):
            return 'Input InChis are stereoisomers'

        #check if compounds are tautomers of each other
        if self.are_tautomers(mol1,mol2):
            return 'Input InChis are tautomers'

        return 'InChis refer to different compounds'
#/////////////////////////////////////////////////////////////////////////iupac comparitor
    def compare_iupac(self,iupac1:str, iupac2:str) -> str:
        if not iupac1.strip() and not iupac2.strip():
            Exception('Empty iupac cannot be compared')
        iupac1 = iupac1.strip()
        iupac2 = iupac2.strip()
        #checks if input iupac strings are identical 
        if self.is_same_string(iupac1,iupac2):
            return 'Input iupac are the same'

        #convert iupac to Mol
        opsin = PyOpsin()
        smile1 = opsin.to_smiles_single(iupac1)
        smile2 = opsin.to_smiles_single(iupac2)

        mol1 = Chem.MolFromInchi(smile1)
        mol2 = Chem.MolFromInchi(smile2)

        #check if iupacs refer to the same compound (compound identical but has different smiles notations)
        if self.is_same_mol(mol1,mol2):
            return 'Input Iupacs refer to the same compound'
        #check if compounds are stereoisomers of each other
        if self.are_stereoisomers(mol1,mol2):
            return 'Input Iupacs are stereoisomers'
        #check if compounds are tautomers of each other
        if self.are_tautomers(mol1,mol2):
            return 'Input Iupacs are tautomers'
        return 'Iupacs refer to different compounds'
#/////////////////////////////////////////////////////////////////////////agnostic comparitor
    def is_same_compound(self,molecule1,molecule2)->bool:
        mol1 = self.make_mol(molecule1)
        mol2 = self.make_mol(molecule2)

        if self.is_same_mol(mol1,mol2):
            return 'Inputs refer to the same compound'

        #check if compounds are stereoisomers of each other
        if self.are_stereoisomers(mol1,mol2):
            return 'Inputs are stereoisomers'

        #check if compounds are tautomers of each other
        if self.are_tautomers(mol1,mol2):
            return 'Inputs are tautomers'

        return 'SMILES refer to different compounds'
#/////////////////////////////////////////////////////////////////////////graphical comparitor (agnostic)
    def draw_differences_fmcs(self,molecule1:str|Chem.Mol,molecule2: str|Chem.Mol): 
        molecule1 = self.make_mol(molecule1)
        molecule2 = self.make_mol(molecule2)
        params = rdFMCS.MCSParameters()

        params.AtomCompareParameters.MatchChiralTag = True
        
        mcs = rdFMCS.FindMCS([molecule1,molecule2],params)
        mcs_smarts = mcs.smartsString
        if mcs_smarts == '':
            return 'No common substructure'
        mcs_mol = Chem.MolFromSmarts(mcs_smarts)
        same1 = molecule1.GetSubstructMatch(mcs_mol)
        highlight1 = []
        same2 = molecule2.GetSubstructMatch(mcs_mol)
        highlight2 = []

        for atom in molecule1.GetAtoms():
            if atom.GetIdx() not in same1:
                highlight1.append(atom.GetIdx())
                
        for atom in molecule2.GetAtoms():
            if atom.GetIdx() not in same2:
                highlight2.append(atom.GetIdx())

        return Draw.MolsToGridImage([molecule1,molecule2], highlightAtomLists=[highlight1,highlight2])

    def draw_differences_rascalMCES(self,molecule1:str|Chem.Mol,molecule2: str|Chem.Mol): 
        pass
        
