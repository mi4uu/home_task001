import moment from 'moment'
import { useParams } from 'react-router-dom'
import { ErrorPage } from '../components/error-page'
import { Loading } from '../components/loading'
import { iFile, iFileContent, useGetFile } from '../store/store'
import { Extend } from './extend'

const DetailsContent = ({ csvFile, csvId }: { csvFile: iFileContent; csvId: number }) => {
  const { columns, data } = csvFile
  return (
    <div className="rg-container">
      <table className="rg-table zebra" summary="Hed">
        <caption className="rg-header">
          <span className="rg-hed">CSV file : {csvFile.file_name}</span>
          <span className="rg-dek">created : {moment(csvFile.created_at).format('YYYY-MM-DD HH:mm')}</span>
		  <div className='componentWrapper'><div className="header">JOIN with external API</div>   <Extend csvFile={csvFile} csvId={csvId} /></div>

       
        </caption>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.id} className="">
              {columns.map((column) => (
                <td key={`${row.id}_${column}`} data-title={column}>
                  {row[column]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <div className="rg-source">
        <span className="pre-colon">SOURCE</span>: <span className="post-colon">Sources</span>
      </div>
    </div>
  )
}

export const Details = () => {
  const { fileId } = useParams()
  const { isLoading, isError, data, error } = useGetFile({ id: parseInt(fileId!, 10) })

  if (isLoading) return <Loading />
  if (isError) return <ErrorPage error={error} />
  return (
    <div className="details">
      <DetailsContent csvFile={data!} csvId={parseInt(fileId!, 10)} />
    </div>
  )
}
