import {
  Create,
  Datagrid,
  Edit,
  EditButton,
  List,
  SimpleForm,
  TextField,
  TextInput,
  BooleanField,
  BooleanInput
} from 'react-admin';

export const ItemList = (props: any) => (
  <List {...props} filters={[]}>
    <Datagrid>
      <TextField source="value" />
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="notes" />
      <TextField source="duration" />
      <BooleanField source="completed" label="Completed" />
      <EditButton />
    </Datagrid>
  </List>
);

export const ItemEdit = (props: any) => (
  <Edit {...props}>
    <SimpleForm>
      <TextInput source="value" />
      <TextInput source="name" />
      <TextInput source="notes" />
      <BooleanInput label="Completed" source="completed" />
    </SimpleForm>
  </Edit>
);

export const ItemCreate = (props: any) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="value" />
      <TextInput source="name" />
      <TextInput source="notes" />
      <TextInput source="duration" />
      <BooleanInput label="Completed" source="completed" />
    </SimpleForm>
  </Create>
);
