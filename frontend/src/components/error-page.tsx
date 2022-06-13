import { Loading } from './loading'

export const ErrorPage = ({ error, isLoading }: { error: Error; isLoading?: boolean }) => {
  return (
    <div>
      {isLoading && <Loading />}
      <h1>Error ({error.name}) :</h1>
      <code>{error.message}</code>
    </div>
  )
}
