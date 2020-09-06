import React, {
  useState,
  useEffect,
  useContext,
} from 'react';
import { Meter, Box, Heading, Text, Button } from 'grommet';

import {Risk, Clusters, Cluster} from './api';
import {getRisk, getClusters, declareCovid} from './api';
import {ClientIdContext, ActionType} from './contexts/clientIdContext';

interface IProps {
  userId: string,
}

export default ({userId}: IProps) => {
  const [risk, setRisk] = useState<Risk>({"user-id": userId, risk: 0});
  const [clusters, setClusters] = useState<Clusters>({
    "user-id": userId,
    clusters: [],
  });
  const [timerId, setTimerId] = useState<NodeJS.Timeout>();

  useEffect(() => {
    if (timerId === undefined) {
       setTimerId(setInterval(() => {
          getRisk(userId).then(setRisk).catch(() => console.log("failed to fetch"));
          getClusters(userId).then(setClusters).catch(() => console.log("failed to fetch clusters"));
        }, 1000))
    } else {
      clearTimeout(timerId)
    }
  }, [userId]);

  const personalInfectiness = !risk.risk ? "being calculated" : risk.risk < 0.4 ? "peacefully low" : risk.risk < 0.8 ? "a little uncomfortable" : "Practically guaranteed";

  const clusterInfos = 
    clusters.clusters
      .sort((a, b) => a.risk - b.risk)
      .map(c => ClusterInfo({cluster: c})) ;
  return <>
    <Heading level="2">Hey {userId}, your chance of getting wrecked is {personalInfectiness}</Heading>
    <Button onClick={() => declareCovid(userId)} primary margin="large" label="I got wrecked"/>
    <Heading level="3">Your social life was easy to determine. Here's each group's infectiness</Heading>
    <Box gap="medium">
      {clusterInfos}
    </Box>
    <Text></Text>
  </>
}

const ClusterInfo = ({cluster}: {cluster: Cluster}) => {
  let text = "";
  let color = "status-ok";
  if (cluster.risk >= 0.7) {
    text = "Avoid.. like the.. plague";
    color = "status-error";
  } else if (cluster.risk >= 0.3) {
    text = "Don't hug";
    color = "status-warning";
  } else {
    text = "Party";
    color = "status-ok";
  }
  const circle = <Meter type="circle" size="xxsmall" thickness="xsmall" round={true} values={[{color, "value": 100*cluster.risk}]} />;
  
  const [clientIdState, clientIdStateDispatch] = useContext(ClientIdContext);
  return <Box 
    direction="column"
    border={{color: color, size: 'medium'}}
    pad="medium"
    round="small"
  >
    <Box direction="row" gap="small">
      {circle}
      <Heading level="4">
        {text} 
      </Heading>
    </Box>
    <Box direction="row" wrap={true} >
      {cluster.friends.map((friend) => <Button 
        key={friend}
        onClick={() => clientIdStateDispatch({action: ActionType.SetClient, clientId: friend})}
        margin="xsmall"
        primary
        label={friend} />
      )}
    </Box>
  </Box>;
}
