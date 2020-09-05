/*
Copyright 2020 The Matrix.org Foundation C.I.C.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

import React from 'react';
import { persistReducer } from './localStorage';
import { object, string, TypeOf } from 'zod';

const STATE_SCHEMA = object({
    clientId: string().nullable(),
});

type State = TypeOf<typeof STATE_SCHEMA>;

// Actions are a discriminated union.
export enum ActionType {
    SetClient = 'SET_CLIENT',
    RemoveClient = 'REMOVE_CLIENT',
}

interface SetClient {
    action: ActionType.SetClient;
    clientId: string;
}

interface RemoveClient {
    action: ActionType.RemoveClient;
}

type Action = SetClient | RemoveClient;

const INITIAL_STATE = {
  clientId: null,
}

export const [initialState, reducer] = persistReducer(
    'client-id',
    INITIAL_STATE,
    STATE_SCHEMA,
    (state: State, action: Action): State => {
        switch (action.action) {
          case ActionType.SetClient:
            return {
              ...state,
              "clientId": action.clientId,
            }
          case ActionType.RemoveClient:
            return {
              ...state,
              "clientId": null,
            }
        }
    }
);

// The defualt reducer needs to be overwritten with the one above
// after it's been put through react's useReducer
export const ClientIdContext = React.createContext<
    [State, React.Dispatch<Action>]
>([initialState, (): void => {}]);

// Quick rename to make importing easier
export const ClientIdProvider = ClientIdContext.Provider;
export const ClientIdConsumer = ClientIdContext.Consumer;

