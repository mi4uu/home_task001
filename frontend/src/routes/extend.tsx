import { useEffect, useState } from 'react'
import { iFile, iFileContent, useExtendFile, useGetRemoteApi } from '../store/store'

const onSelectColumn =
  (setColumn: React.Dispatch<React.SetStateAction<string>>) => (e: React.ChangeEvent<HTMLSelectElement>) => {
    setColumn(e.target.value)
  }

const ExtendCallComponent = (props: {
  url: string
  csv_id: number | string
  csv_column: string
  api_column: string
}) => {
  const mutation = useExtendFile(props)
  return (
    <button
      className="buttonSml primary"
      style={{ marginTop: 30 }}
      onClick={async () => {
        const result = await mutation.mutateAsync()
        if (result.id) {
          alert('File extended successfully! now You will be redirected to new file')

          window.location.href = `/file/${result.id}`
        } else {
          alert(`Something went wrong! ${mutation.error?.message}`)
        }
      }}
    >
      join and save as new file
    </button>
  )
}
export const Extend = ({ csvFile, csvId }: { csvFile: iFileContent; csvId: number }) => {
  const [url, setUrl] = useState<string | null>(null)
  const ApiMutation = useGetRemoteApi({ url: url ?? '' })
  const [file, setFile] = useState<iFile | null>(null)
  const [column0, setColumn0] = useState<string>(csvFile.columns[0])
  const [column1, setColumn1] = useState<string>(file?.columns[0] ?? '')
  useEffect(() => {
    if (file) setColumn1(file.columns[0] ?? '')
  }, [file])

  if (ApiMutation.isLoading) return <div>Loading...</div>

  return (
    <div style={{ marginTop: 40 }}>
      {!file ? (
        <label style={{ marginRight: 10 }}>
          API URL: <input name="url" onChange={(event) => setUrl(event.target.value)}></input>
        </label>
      ) : (
        <b>url: {url}</b>
      )}
      {!file && (
        <button
          className="buttonSml primary"
          onClick={async () => {
            const result = await ApiMutation.mutateAsync()
            setFile(result)
          }}
        >
          get columns
        </button>
      )}

      {file && (
        <div style={{ marginTop: 30 }}>
          Select columns to join by
          <label
            style={{
              display: 'block',
              marginLeft: 20,
            }}
          >
            {' '}
            <b>THIS</b> file column:{' '}
            <select onChange={onSelectColumn(setColumn0)} style={{ marginLeft: 40 }}>
              {csvFile.columns.map((column) => (
                <option>{column}</option>
              ))}
            </select>
          </label>
          <label
            style={{
              display: 'block',
              marginLeft: 20,
            }}
          >
            {' '}
            <b>API column:</b>{' '}
            <select onChange={onSelectColumn(setColumn1)} style={{ marginLeft: 40 }}>
              {file.columns.map((column) => (
                <option>{column}</option>
              ))}
            </select>
          </label>
          {column0 && column1 && url && (
            <ExtendCallComponent url={url} csv_id={csvId} api_column={column1} csv_column={column0} />
          )}
        </div>
      )}
    </div>
  )
}
