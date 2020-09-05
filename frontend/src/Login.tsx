import React, { useContext, useState } from 'react';

import {ClientIdContext, ActionType} from './contexts/clientIdContext';
import { Form, FormField, TextInput, Button } from 'grommet';

export default () => {
  const [_, clientIdDispatch] = useContext(ClientIdContext); 

  return <div>
    <h1>Covid Social Alert</h1>
    <Form onSubmit={({value}) => clientIdDispatch({
      action: ActionType.SetClient,
      // @ts-ignore
      clientId: value.clientId,
    })} > 
      <FormField name="clientId" label="Name">
        <TextInput id="textinput-id" name="clientId" />
      </FormField>
      <Button type="submit" primary label="Go" />
    </Form>
  </div>;
}
