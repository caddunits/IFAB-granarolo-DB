from collections import OrderedDict

commands = OrderedDict({
    'Units':
    """CREATE TABLE IF NOT EXISTS Units (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL
    );""",

    'Universities':
    """CREATE TABLE IF NOT EXISTS Universities (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL
    );""",

    'Groups':
    """CREATE TABLE IF NOT EXISTS Groups (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Website TEXT
    );""",

     'University_Group':
    """CREATE TABLE IF NOT EXISTS University_Group (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Group_ID INTEGER NOT NULL,
        University_ID INTEGER NOT NULL,
        FOREIGN KEY (Group_ID) REFERENCES Groups(ID),
        FOREIGN KEY (University_ID) REFERENCES Universities(ID),
        UNIQUE (Group_ID, University_ID)
    );""",

    'Expertises':
    """CREATE TABLE IF NOT EXISTS Expertises (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Description TEXT NOT NULL
    );""",

    'Researchers':
    """CREATE TABLE IF NOT EXISTS Researchers (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        FullName TEXT NOT NULL,
        Email TEXT NOT NULL,
        Group_ID INTEGER NOT NULL,
        FOREIGN KEY (Group_ID) REFERENCES Groups(ID),
        UNIQUE (ID, Group_ID)
    );""",

    'Unit_Researcher':
    """CREATE TABLE IF NOT EXISTS Unit_Researcher (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Unit_ID INTEGER NOT NULL,
        Researcher_ID INTEGER NOT NULL,
        FOREIGN KEY (Unit_ID) REFERENCES Units(ID),
        FOREIGN KEY (Researcher_ID) REFERENCES Researchers(ID),
        UNIQUE (Unit_ID, Researcher_ID)
    );""",

    'Researcher_Expertise':
    """CREATE TABLE IF NOT EXISTS Researcher_Expertise (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Researcher_ID INTEGER NOT NULL,
        Expertise_ID INTEGER NOT NULL,
        FOREIGN KEY (Researcher_ID) REFERENCES Researchers(ID),
        FOREIGN KEY (Expertise_ID) REFERENCES Expertises(ID),
        UNIQUE (Researcher_ID, Expertise_ID)
    );""",

    'Literature':
    """CREATE TABLE IF NOT EXISTS Literature(
     ID INTEGER PRIMARY KEY AUTOINCREMENT,
     Title TEXT NOT NULL,
     PaperDOI TEXT NOT NULL
    );""",
    
    'PropClasses': 
"""CREATE TABLE IF NOT EXISTS PropClasses(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT NOT NULL,
  UNIQUE (Name)
);""",

'Properties': 
"""CREATE TABLE IF NOT EXISTS Properties(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT NOT NULL,
  IsKPI TEXT NOT NULL,
  Doi TEXT,
  Class_ID INTEGER NOT NULL,
  FOREIGN KEY (Class_ID) REFERENCES PropClasses(ID),
  UNIQUE (Name),
  UNIQUE (ID, Class_ID)
);""",

'Polymers': 
"""CREATE TABLE IF NOT EXISTS Polymers(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT NOT NULL,
  UNIQUE (Name)
);""",

'Polymer_Property':
    """CREATE TABLE IF NOT EXISTS  Polymer_Property(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Polymer_ID INTEGER NOT NULL,
        Property_ID INTEGER NOT NULL,
        FOREIGN KEY (Polymer_ID) REFERENCES Polymers(ID),
        FOREIGN KEY (Property_ID) REFERENCES Properties(ID),
        UNIQUE (Polymer_ID, Property_ID)
    );""",

'ForceFields': 
"""CREATE TABLE IF NOT EXISTS ForceFields(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT NOT NULL,
  Details TEXT,
  Doi TEXT
);""",

'Group_use_FF':
"""CREATE TABLE IF NOT EXISTS Group_use_FF
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Group_ID INTEGER NOT NULL,
  ForceField_ID INTEGER NOT NULL,
  FOREIGN KEY (Group_ID) REFERENCES Groups(ID),
  FOREIGN KEY (ForceField_ID) REFERENCES ForceFields(ID),
  UNIQUE (Group_ID, ForceField_ID)
);""",

'Group_develop_FF':
"""CREATE TABLE IF NOT EXISTS Group_develop_FF
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  ForceField_ID INTEGER NOT NULL,
  Group_ID INTEGER NOT NULL,
  FOREIGN KEY (Group_ID) REFERENCES Groups(ID),
  FOREIGN KEY (ForceField_ID) REFERENCES ForceFields(ID),
  UNIQUE (Group_ID, ForceField_ID)
);""",

'Software': 
"""CREATE TABLE IF NOT EXISTS Software
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT NOT NULL,
  Details TEXT,
  Website TEXT,
  Provider TEXT
);""",

'Hardware': 
"""CREATE TABLE IF NOT EXISTS Hardware
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT NOT NULL,
  Details TEXT
);""",

'Roles':
"""CREATE TABLE IF NOT EXISTS Roles
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Role TEXT NOT NULL
);""",

'Models':
"""CREATE TABLE IF NOT EXISTS Models
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Model TEXT NOT NULL
);""",

'Laws':
"""CREATE TABLE IF NOT EXISTS Laws
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Law TEXT NOT NULL
);""",

'SmallMolecules':
"""CREATE TABLE IF NOT EXISTS SmallMolecules
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  SMILES TEXT NOT NULL,
  IUPACName TEXT NOT NULL
);""",

'Mol_Role':
"""CREATE TABLE IF NOT EXISTS Mol_Role
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  SmallMolecule_ID INTEGER NOT NULL,
  Role_ID INTEGER NOT NULL,
  FOREIGN KEY (SmallMolecule_ID) REFERENCES SmallMolecules(ID),
  FOREIGN KEY (Role_ID) REFERENCES Roles(ID),
  UNIQUE (SmallMolecule_ID, Role_ID)
);""",

'Mol_to_Polymer':
"""CREATE TABLE IF NOT EXISTS Mol_to_Polymer
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  SmallMolecule_ID INTEGER NOT NULL,
  Polymer_ID INTEGER NOT NULL,
  FOREIGN KEY (SmallMolecule_ID) REFERENCES SmallMolecules(ID),
  FOREIGN KEY (Polymer_ID) REFERENCES Polymers(ID),
  UNIQUE (SmallMolecule_ID, Polymer_ID)
);""",

'Mol_predicted_by_Model':
"""CREATE TABLE IF NOT EXISTS Mol_predicted_by_Model
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Value INTEGER,
  Classification TEXT,
  SmallMolecule_ID INTEGER NOT NULL,
  Model_ID INTEGER NOT NULL,
  FOREIGN KEY (SmallMolecule_ID) REFERENCES SmallMolecules(ID),
  FOREIGN KEY (Model_ID) REFERENCES Models(ID),
  UNIQUE (SmallMolecule_ID, Model_ID)
);""",

'Mol_present_in_Law':
"""CREATE TABLE IF NOT EXISTS Mol_present_in_Law
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Present TEXT NOT NULL,
  SmallMolecule_ID INTEGER NOT NULL,
  Law_ID INTEGER NOT NULL,
  FOREIGN KEY (SmallMolecule_ID) REFERENCES SmallMolecules(ID),
  FOREIGN KEY (Law_ID) REFERENCES Laws(ID),
  UNIQUE (SmallMolecule_ID, Law_ID)
);""",

'Predictions':
"""CREATE TABLE IF NOT EXISTS Predictions
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Value FLOAT,
  Unit TEXT,
  Error FLOAT,
  Property_ID INTEGER NOT NULL,
  FOREIGN KEY (Property_ID) REFERENCES Properties(ID),
  UNIQUE (ID, Property_ID)
);""",

'CalculationClasses':
"""CREATE TABLE IF NOT EXISTS CalculationClasses
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Class TEXT NOT NULL
);""",

'CalculationModels':
"""CREATE TABLE IF NOT EXISTS CalculationModels
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Model TEXT NOT NULL
);""",

'Workflows':
"""CREATE TABLE IF NOT EXISTS Workflows
( 
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Workflow TEXT NOT NULL,
  Prediction_ID INTEGER NOT NULL,
  FOREIGN KEY (Prediction_ID) REFERENCES Predictions(ID),
  UNIQUE (ID, Prediction_ID)
);""",

'Literature_ForceFields':
"""CREATE TABLE IF NOT EXISTS Literature_ForceFields
(
 ID INTEGER PRIMARY KEY AUTOINCREMENT,
 Literature_ID INTEGER NOT NULL,
 ForceField_ID INTEGER NOT NULL,
 FOREIGN KEY (Literature_ID) REFERENCES Literature(ID),
 FOREIGN KEY (ForceField_ID) REFERENCES ForceFields(ID),
 UNIQUE (ForceField_ID, Literature_ID)
);""",

'Literature_Properties':
"""CREATE TABLE IF NOT EXISTS Literature_Properties
(
 ID INTEGER PRIMARY KEY AUTOINCREMENT,
 Literature_ID INTEGER NOT NULL,
 Property_ID INTEGER NOT NULL,
 FOREIGN KEY (Property_ID) REFERENCES Property(ID),
 FOREIGN KEY (Literature_ID) REFERENCES Literature(ID),
 UNIQUE (Property_ID, Literature_ID)
 );""",

 'Nodes':
 """CREATE TABLE  IF NOT EXISTS Nodes
            (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Node TEXT NOT NULL,
            UNIQUE (Node)
            );""",

  'Edges':
  """CREATE TABLE IF NOT EXISTS Edges
            (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Input_ID INTEGER NOT NULL,
            Output_ID INTEGER NOT NULL,
            FOREIGN KEY (Input_ID) REFERENCES Nodes(ID),
            FOREIGN KEY (Output_ID) REFERENCES Nodes(ID),
            UNIQUE(Input_ID, Output_ID)
            );""",

  'Workflow_Edges':
  """CREATE TABLE IF NOT EXISTS Workflow_Edges
            (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Workflow_ID INTEGER NOT NULL, 
            Edge_ID INTEGER NOT NULL, 
            StepNumber INTEGER NOT NULL, 
            FOREIGN KEY (Workflow_ID) REFERENCES Workflows(ID),  
            FOREIGN KEY (Edge_ID) REFERENCES Edges(ID), 
            UNIQUE(Workflow_ID, Edge_ID)
            );""",

  'Calculations':
  """CREATE TABLE IF NOT EXISTS Calculations
            (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Details TEXT,
            System TEXT NOT NULL,
            LinkToData TEXT,
            Class_ID INTEGER NOT NULL,
            Model_ID INTEGER NOT NULL,
            Edge_ID INTEGER,
            Group_ID INTEGER NOT NULL,
            ForceField_ID INTEGER,
            Software_ID INTEGER NOT NULL,
            Polymer_ID INTEGER NOT NULL,
            Hardware_ID INTEGER NOT NULL,
            FOREIGN KEY (Class_ID) REFERENCES CalculationClasses(ID),
            FOREIGN KEY (Model_ID) REFERENCES CalculationModels(ID),
            FOREIGN KEY (Edge_ID) REFERENCES Edges(ID),
            FOREIGN KEY (Group_ID) REFERENCES Groups(ID),
            FOREIGN KEY (ForceField_ID) REFERENCES ForceFields(ID),
            FOREIGN KEY (Software_ID) REFERENCES Software(ID),
            FOREIGN KEY (Polymer_ID) REFERENCES Polymers(ID),
            FOREIGN KEY (Hardware_ID) REFERENCES Hardware(ID),
            UNIQUE (Class_ID, Model_ID, Edge_ID, Group_ID, ForceField_ID, Software_ID, Polymer_ID, Hardware_ID)
            );"""
})


