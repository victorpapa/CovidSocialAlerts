import React, {
  useContext,
} from 'react';
import { Grommet, Main, Heading, Box } from 'grommet';

import GlobalContext from './contexts/GlobalContext';
import { ClientIdContext } from './contexts/clientIdContext';
import Login from './Login';
import RiskOMeter from './RiskOMeter';

const theme = {
  global: {
    font: {
      family: 'Roboto',
      size: '18px',
      height: '20px',
    },
  },
};

function App() {
  const [clientIdState] = useContext(ClientIdContext);
  console.log(clientIdState)

  let app: JSX.Element;

  if (clientIdState.clientId) {
    app = <RiskOMeter userId={clientIdState.clientId} />
  } else {
    app = <Login />;
  }

  return (
    <Grommet theme={theme}>
    <GlobalContext>
      <Main>
        <Box
          border={{ color: 'brand', size: 'large' }}
          pad="medium"
          gap="medium"
        >
          {app}
        </Box>
      </Main>
    </GlobalContext>
    </Grommet>
  );
}

export default App;
