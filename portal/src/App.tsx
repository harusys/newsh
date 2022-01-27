import { VFC, useState, useEffect } from 'react'
// import { forwardRef } from 'react';
// import Avatar from 'react-avatar';
// import Grid from '@material-ui/core/Grid'

// import MaterialTable from "material-table";
// import AddBox from '@material-ui/icons/AddBox';
// import ArrowDownward from '@material-ui/icons/ArrowDownward';
// import Check from '@material-ui/icons/Check';
// import ChevronLeft from '@material-ui/icons/ChevronLeft';
// import ChevronRight from '@material-ui/icons/ChevronRight';
// import Clear from '@material-ui/icons/Clear';
// import DeleteOutline from '@material-ui/icons/DeleteOutline';
// import Edit from '@material-ui/icons/Edit';
// import FilterList from '@material-ui/icons/FilterList';
// import FirstPage from '@material-ui/icons/FirstPage';
// import LastPage from '@material-ui/icons/LastPage';
// import Remove from '@material-ui/icons/Remove';
// import SaveAlt from '@material-ui/icons/SaveAlt';
// import Search from '@material-ui/icons/Search';
// import ViewColumn from '@material-ui/icons/ViewColumn';
import axios from 'axios'
// import Alert from '@material-ui/lab/Alert';

const api = axios.create({
  baseURL: `https://reqres.in/api`,
})

const App: VFC = () => {
  type IType = 'string' | 'boolean' | 'numeric' | 'date' | 'datetime' | 'time' | 'currency'
  const string: IType = 'string'

  const columns = useState([
    { title: 'Name', field: 'name', type: 'string' as const },
    {
      title: 'Surname',
      field: 'surname',
      initialEditValue: 'initial edit value',
      type: 'string' as const,
    },
    { title: 'Birth Year', field: 'birthYear', type: 'string' as const },
    {
      title: 'Birth Place',
      field: 'birthCity',
      lookup: { 34: 'İstanbul', 63: 'Şanlıurfa' },
      type: 'string' as const,
    },
  ])

  const [data, setData] = useState([
    {
      name: 'Mehmet',
      surname: 'Baran',
      birthYear: 1987,
      birthCity: 63,
      type: string,
    },
    {
      name: 'Zerya Betül',
      surname: 'Baran',
      birthYear: 2017,
      birthCity: 34,
      type: string,
    },
  ])

  // for error handling
  const [iserror, setIserror] = useState(false)
  const [errorMessages, setErrorMessages] = useState([])

  useEffect(() => {
    api
      .get('/users')
      .then((res) => {
        setData(res.data.data)
      })
      .catch((error) => {
        console.log('Error')
      })
  }, [])

  const handleRowUpdate = (newData, oldData, resolve) => {
    // validation
    const errorList = []
    if (newData.name === '') {
      errorList.push('Please enter name')
    }
    if (newData.surname === '') {
      errorList.push('Please enter surname')
    }

    if (errorList.length < 1) {
      api
        .patch(`/users/${newData.id}`, newData)
        .then((res) => {
          const dataUpdate = [...data]
          const index = oldData.tableData.id
          dataUpdate[index] = newData
          setData([...dataUpdate])
          resolve()
          setIserror(false)
          setErrorMessages([])
        })
        .catch((error) => {
          setErrorMessages(['Update failed! Server error'])
          setIserror(true)
          resolve()
        })
    } else {
      setErrorMessages(errorList)
      setIserror(true)
      resolve()
    }
  }

  const handleRowAdd = (newData, resolve) => {
    // 検証
    const errorList = []
    if (newData.name === undefined) {
      errorList.push('名を入力してください')
    }
    if (newData.name === undefined) {
      errorList.push('名を入力してください')
    }
    if (errorList.length < 1) {
      // エラー
      api
        .post('/ users', newData)
        .then((res) => {
          const dataToAdd = [...data]
          dataToAdd.push(newData)
          setData(dataToAdd)
          resolve()
          setErrorMessages([])
          setIserror(false)
        })
        .catch((error) => {
          setErrorMessages(['Cannotadddata。Servererror！'])
          setIserror(true)
          resolve()
        })
    } else {
      setErrorMessages(errorList)
      setIserror(true)
      resolve()
    }
  }

  return (
    <div className="App">
      <h1>Hello CodeSandbox</h1>
      <h2>Start editing to see some magic happen!</h2>

      <MaterialTable
        title="Editable Preview"
        columns={columns}
        data={data}
        editable={{
          onRowAdd: (newData) =>
            new Promise((resolve) => {
              setTimeout(() => {
                setData([...data, newData])

                resolve()
              }, 1000)
            }),
          onRowUpdate: (newData, oldData) =>
            new Promise((resolve, reject) => {
              setTimeout(() => {
                const dataUpdate = [...data]
                const index = oldData.tableData.id
                dataUpdate[index] = newData
                setData([...dataUpdate])

                resolve()
              }, 1000)
            }),
          onRowDelete: (oldData) =>
            new Promise((resolve, reject) => {
              setTimeout(() => {
                const dataDelete = [...data]
                const index = oldData.tableData.id
                dataDelete.splice(index, 1)
                setData([...dataDelete])

                resolve()
              }, 1000)
            }),
        }}
      />
    </div>
  )
}

export default App
