import React, {
  useContext,
} from 'react';
import { Heading, Grommet, Main } from 'grommet';

import GlobalContext from './contexts/GlobalContext';
import { ClientIdContext } from './contexts/clientIdContext';
import Login from './Login';
import RiskOMeter from './RiskOMeter';

const theme = {
  global: {
    font: {
      family: 'Titillium Web',
      size: '18px',
      height: '20px',
    },
  },
};

function App() {
  const [clientIdState] = useContext(ClientIdContext);

  let app: JSX.Element;

  if (clientIdState.clientId) {
    app = <RiskOMeter userId={clientIdState.clientId} />
  } else {
    app = <Login />;
  }

  return (
    <Grommet theme={theme}>
    <GlobalContext>
      <Main alignContent="center" animation="fadeIn" margin="large">
        <Heading>Covid Infectiness</Heading>
        {app}
      </Main>
    </GlobalContext>
    </Grommet>
  );
}

export default App;
