import React, {useState} from 'react'
import prettyBytes from 'pretty-bytes'

const FileUpload = () => {
	const [selectedFile, setSelectedFile] = useState<File | null>()
    const [isUploading, setIsUploading] = useState<boolean>(false)

	const changeHandler = (event:React.ChangeEvent<HTMLInputElement>) => {
        const {files} = event.target

        if (files && files.length > 0) 
		    setSelectedFile(files[0])
        else alert('No file selected')
	}

	const handleSubmission = () => {
		const formData = new FormData()
        if(!selectedFile) return alert('No file selected')

		formData.append('file', selectedFile)
        setIsUploading(true)
		fetch(
			'/api/files/',
			{
				method: 'POST',
				body: formData,
			}
		)
			.then((response) => response.json())
			.then((result) => {
				console.log('Success:', result)
			})
			.catch((error) => {
				console.error('Error:', error)
                alert(error)
			}).finally(() => {
                setIsUploading(false)
                setSelectedFile(null)
            })
	}
	

	return(
   <div>
			<input  type="file" name="file" onChange={changeHandler} accept=".csv" />
			{selectedFile ? (
				<div>
					<p><b>Filename</b>: {selectedFile.name}</p>
					<p><b>Filetype</b>: {selectedFile.type}</p>
					<p><b>Size</b>: {prettyBytes(selectedFile.size)}</p>
				
				</div>
			) : (
				<p>Select a file to show details</p>
			)}
			<div>
			{selectedFile && !isUploading &&	<button onClick={handleSubmission} className="button primary">Submit</button>}
            {isUploading && <p>Uploading...</p>}
			</div>
		</div>
	)
}

export default function Upload() {
    return (
      <main style={{ padding: "1rem 0" }}>
        <h2>Upload</h2>
        <FileUpload />
      </main>
    );
  }