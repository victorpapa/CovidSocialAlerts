import React, {
  useState,
  useEffect,
} from 'react';
import {Box, Heading, Text} from 'grommet';
import chance from 'chance';

import {Risk, Clusters, Cluster} from './api';
import {getRisk, getClusters} from './api';

const Chance = chance();

interface IProps {
  userId: string,
}

export default ({userId}: IProps) => {
  const userIdInt = parseInt(userId);
  const [risk, setRisk] = useState<Risk>({"user-id": userIdInt, risk: 0});
  const [clusters, setClusters] = useState<Clusters>({
    "user-id": userIdInt,
    clusters: [],
  });

  useEffect(() => {
    getRisk(userId).then(setRisk).catch(() => console.log("failed to fetch"));
    getClusters(userId).then(setClusters).catch(() => console.log("failed to fetch clusters"));
  }, [userId]);

  const clusterDiv = clusters.clusters.map(c => ClusterInfo({cluster: c}));
  return <>
    <Heading>Hello {userId}</Heading>
    <Text>Risk of getting covid: {risk.risk}</Text>
    {clusterDiv}
    <Text></Text>
  </>
}

const ClusterInfo = ({cluster}: {cluster: Cluster}) => {
  let text = "";
  if (cluster.risk >= 0.7) {
    text = "It's not safe to hang out with this group";
  } else if (cluster.risk >= 0.4) {
    text = "Just be carefull round these people yo";
  } else {
    text = "This group seems chill";
  }
  return <Box 
    direction="column"
    border={{color: 'brand', size: 'medium'}}
    pad="medium"
  >
    <Text>
      {text}
    </Text>
    <Box direction="row" gap="small">
      {cluster.friends.map(() => <Box>{Chance.name()}</Box>)}
    </Box>
  </Box>;
}
