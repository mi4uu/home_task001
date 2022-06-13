import moment from 'moment'
import { ErrorPage } from '../components/error-page'
import { Loading } from '../components/loading'
import { useGetFiles } from '../store/store'
import prettyBytes from 'pretty-bytes'
import { Link } from 'react-router-dom'

export default function List() {
  const { data, isLoading, error } = useGetFiles()

  if (error) return <ErrorPage error={error} isLoading={isLoading} />

  if (isLoading) return <Loading />
  return (
    <div className="rg-container">
      <table className="rg-table zebra" summary="Hed">
        <caption className="rg-header">
          <span className="rg-hed">files list </span>
        </caption>
        <thead>
          <tr>
            <th>Name</th>
            <th>Date</th>
            <th>Size</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {data?.map((csvFile) => (
            <tr key={csvFile.id}>
              <td data-title="name">{csvFile.file_name}</td>
              <td data-title="date">{moment(csvFile.created_at).format('YYYY-MM-DD HH:mm')}</td>
              <td data-title="size">{prettyBytes(csvFile.file_size)}</td>
              <td>
                <Link to={`/file/${csvFile.id}`}>
                  <button className="button buttonSml">show</button>
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
