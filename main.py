from script.create_db import del_database, add_tables
from script.fill_tables.fill_db import fill_table
from script.paths import excel_file, db_file

file_path = excel_file

def flow(name, reset=False):
   '''Database creation and filling control room'''

   db_path = db_file
       
   try:
      if reset:
            del_database(path=db_path)
            add_tables(path=db_path)
            print('Database reboot')

      fill_table(path=db_path, name=name, file_path=file_path)

   except Exception as e:
        print(f'{e}')
   
#Tables filling must follow a precise order due to FK dependencies!!
if __name__=='__main__':
          
        flow(name='Universities', reset=True)
        flow(name='Groups', reset=False)
        flow(name='University_Group', reset=False) #FK to Universities and Groups
        flow(name='Researchers', reset=False) #FK to Groups
        flow(name='Expertises', reset=False)
        flow(name='Researcher_Expertise', reset=False) #FK to Researchers and Groups
        flow(name='Units', reset=False)
        flow(name='Unit_Researcher', reset=False) #FK to Researchers and Units

        flow(name='ForceFields', reset=False)
        flow(name='Group_use_FF', reset=False) #FK to Units and ForceFields
        flow(name='Group_develop_FF', reset=False) #FK to Groups and ForceFields

        #flow(name='Models', reset=False)
        #flow(name='Roles', reset=False)
        #flow(name='Laws', reset=False)
        #flow(name='SmallMolecules', reset=False) #FK to Roles
        #flow(name='Mol_predicted_by_Model', reset=False) #FK to Models and SmallMolecules
        #flow(name='Mol_present_in_Law', reset=False) #FK to Laws and SmallMolecules
        #flow(name='Mol_Role', reset=False) #FK to Laws and SmallMolecules

        flow(name='Polymers', reset=False)
        #flow(name='Mol_to_Polymer', reset=False) #FK to Polymers and SmallMolecules

        flow(name='PropClasses', reset=False)
        flow(name='Properties', reset=False) #FK to PropClasses

        flow(name='Polymer_Property', reset=False) #FK to Polymers and Properties

        flow(name='Literature', reset=False)
        #flow(env='test', name='Literature_Properties', reset=False) #FK to Literature and Properties
        flow(name='Literature_ForceFields', reset=False) #FK to Literature and ForceFields

        flow(name='Predictions', reset=False) #FK to Properties
        
        flow(name='Workflows', reset=False) #FK to Predictions
        flow(name='Graphs', reset=False) #FK to Workflows (multiple tables filling!)

        flow(name='Hardware', reset=False)
        flow(name='Software', reset=False)
        flow(name='CalculationClasses', reset=False)
        flow(name='CalculationModels', reset=False)

        flow(name='Calculations', reset=False) #FK to CalculationClasses, CalculationModels, Hardware, Software, ForceFields, Edges(Graphs) and Polymers



        
   
