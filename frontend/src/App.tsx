import { useState } from 'react'
import {
  Routes,
  Route,
} from "react-router-dom"
import { Link } from 'react-router-dom'
import logo from './logo.svg'
import { Details } from './routes/details'
import List from './routes/list'
import Upload from './routes/upload'
import listIcon from './static/list.png'
import uploadIcon from './static/upload.png'

const Placeholder = () => <h3 style={{textAlign:'center'}}><img src="https://c.tenor.com/y6_NBi-9ZLQAAAAC/skyrim-margin.gif" alt="welcome"/></h3>

function App() {

  return (
    <div className="App">
      <header className="App-header">
        
        <h1 className="logoWrap"> <img src={logo} className="logo" alt="logo" /> CSV TOOL</h1>
        <h1  className="menuWrap">
        <Link to="/files">   <button className="button"><img src={listIcon} alt="list" /> LIST</button></Link>
        <Link to="/upload">  <button className="button"><img src={uploadIcon} alt="upload new csv file" /> NEW</button></Link>
        </h1>
     
      </header>
      <div className="appBody">
    <Routes>
      <Route path="/" element={<Placeholder />} />
      <Route path="files" element={<List />} />
      <Route path="file">
      <Route path=":fileId" element={<Details />} />
      </Route>
      <Route path="upload" element={<Upload />} />
      <Route path="*" element={<Placeholder />} />
    </Routes>

      </div>
    </div>
  )
}

export default App
