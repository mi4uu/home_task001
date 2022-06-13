import { QueryClient, useMutation, useQuery } from 'react-query'
import { fetchWithTimeout } from './utils'
 
 export const queryClient = new QueryClient()

 export interface iFile {
    id: number
    file_name: string
    file_path: string
    file_size: number
    created_at:string
    columns: string[]
 }


 export interface iFileContent {
    columns: string[]
    created_at: string
    data: Array<{[key:string]:string|number|null}>
    file_name: string
    file_size: number
    file_src: string
    schema: {
        fields: Array<{name: string, type: string}>
        pandas_version: string
        primaryKey: string[]
    }
 }
 
 export const fetchFiles = async () => {
   const response = await fetchWithTimeout('/api/files/')
   return response.json()
 }

 export const useGetFiles = ()=>useQuery<iFile[], Error>('files', fetchFiles)


 export const fetchFileById = async (id:number) => {
    const response = await fetchWithTimeout(`/api/files/${id}`)
    return response.json()
  }

export const useGetFile = ({id}:{id:number}) => useQuery<iFileContent, Error>(['file', id], ()=> fetchFileById(id))

    export const fetchRemoteApi = async (url:string) => {
        const response = await fetch(`/api/remote_api/?url=${url}`, {
            method: 'POST',
            headers: {
                'content-type': 'application/json',
                'accept': 'application/json',
              },
        })
        return response.json()
    }
export const useGetRemoteApi = ({url}:{url:string}) => useMutation<iFile, Error>(['remoteApi', url], ()=> fetchRemoteApi(url))

export const extendFile = async (params:{url:string, csv_id:string, csv_column:string, api_column:string}) => {
    const response = await fetch(`/api/remote_api/extend?${new URLSearchParams(params).toString()}`, {
        method: 'POST',
        headers: {
            'content-type': 'application/json',
            'accept': 'application/json',
          },
    })
    return response.json()
}
export const useExtendFile = ({url,csv_id,csv_column, api_column}:{url:string, csv_id:number|string, csv_column:string, api_column:string}) => useMutation<iFile, Error>(['remoteApi', url,csv_id,csv_column, api_column], ()=> extendFile({url, csv_id: `${csv_id}`, csv_column, api_column}))