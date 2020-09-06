import { object, array, string, number, TypeOf } from 'zod';

/*
 * If the condition is false reject with rejectReason
 * If it's true resolve with the result = resultThunk()
 */
export function ensure<T>(condition: boolean, resultThunk: () => T | PromiseLike<T>, rejectReason?: string) {
    return condition
        ? Promise.resolve(resultThunk())
        : Promise.reject(new Error(rejectReason));
}

export function parseJSON(resp: Response) {
    return ensure(
        resp.ok,
        () => resp.json(),
        `Error from Homeserver. Error code: ${resp.status}`,
    );
}

const clusterSchema = object({
  friends: array(string()),
  risk: number(),
});

const clustersSchema = object({
  "user-id": string(),
  "clusters": array(clusterSchema),
});

export type Clusters = TypeOf<typeof clustersSchema>;
export type Cluster = TypeOf<typeof clusterSchema>;

export function getClusters(userId: string) {
  return fetch(`http://localhost:8000/clusters/${userId}`)
    .then(parseJSON)
    .then(clustersSchema.parse)
}

const riskSchema = object({
  "user-id": string(),
  "risk": number().refine(x => 0 <= x && x <= 1, {
    message: "Risk must be a number between 0 and 1",
  }),
});

export type Risk = TypeOf<typeof riskSchema>;

export function getRisk(userId: string) {
  return fetch(`http://localhost:8000/risk/${userId}`)
    .then(parseJSON)
    .then(riskSchema.parse)
}

export function declareCovid(userId: string) {
  return fetch(`http://localhost:8000/gotit/${userId}`);
}

const daysSinceSchema = number();

export type DaysSince = TypeOf<typeof daysSinceSchema>

export function getDaysSince(userId: string) {
  return fetch(`http://localhost:8000/dayssince/${userId}`)
  .then(parseJSON)
  .then(daysSinceSchema.parse);
}
