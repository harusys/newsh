import { VFC, useState, useEffect, forwardRef } from 'react'
// import Avatar from 'react-avatar';
// import Grid from '@material-ui/core/Grid'

import MaterialTable, { Icons } from 'material-table'
import AddBox from '@material-ui/icons/AddBox'
import ArrowDownward from '@material-ui/icons/ArrowDownward'
import Check from '@material-ui/icons/Check'
import ChevronLeft from '@material-ui/icons/ChevronLeft'
import ChevronRight from '@material-ui/icons/ChevronRight'
import Clear from '@material-ui/icons/Clear'
import DeleteOutline from '@material-ui/icons/DeleteOutline'
import Edit from '@material-ui/icons/Edit'
import FilterList from '@material-ui/icons/FilterList'
import FirstPage from '@material-ui/icons/FirstPage'
import LastPage from '@material-ui/icons/LastPage'
import Remove from '@material-ui/icons/Remove'
import SaveAlt from '@material-ui/icons/SaveAlt'
import Search from '@material-ui/icons/Search'
import ViewColumn from '@material-ui/icons/ViewColumn'
import axios from 'axios'

const tableIcons: Icons = {
  /* eslint-disable react/jsx-props-no-spreading */
  Add: forwardRef((props, ref) => <AddBox {...props} ref={ref} />),
  Check: forwardRef((props, ref) => <Check {...props} ref={ref} />),
  Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref} />),
  DetailPanel: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
  Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} />),
  Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref} />),
  Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref} />),
  FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} />),
  LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} />),
  NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
  PreviousPage: forwardRef((props, ref) => <ChevronLeft {...props} ref={ref} />),
  ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Search: forwardRef((props, ref) => <Search {...props} ref={ref} />),
  SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref} />),
  ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref} />),
  ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref} />),
  /* eslint-enable react/jsx-props-no-spreading */
}

const api = axios.create({
  responseType: 'json',
})

export type ModelItem = Pick<Model, 'id' | 'user_id' | 'task_name' | 'scheduled_at'>

export interface Model {
  id: string
  user_id: string
  task_name: string
  scheduled_at: string
}

const App: VFC = () => {
  type IType = 'string' | 'boolean' | 'numeric' | 'date' | 'datetime' | 'time' | 'currency'
  const string: IType = 'string'

  const [columns, setColumns] = useState([
    { title: 'ID', field: 'id' },
    { title: 'ユーザID', field: 'user_id', hidden: true },
    { title: 'コンテンツ名', field: 'task_name' },
    { title: '通知時刻', field: 'scheduled_at' },
  ])

  const [data, setData] = useState<Array<ModelItem>>([])

  // for error handling
  const [iserror, setIserror] = useState(false)
  const [errorMessages, setErrorMessages] = useState<Array<string>>([])

  useEffect(() => {
    api
      .get<Array<Model>>('/api/timer-manager/Ud9f705bf1ae17b6111b1b5353b00eaf7')
      .then((response) => {
        setData(
          response.data.map<ModelItem>((d) => ({
            id: d.id,
            user_id: d.user_id,
            task_name: d.task_name,
            scheduled_at: d.scheduled_at,
          }))
        )
      })
      .catch((e: unknown) => {
        if (e instanceof Error) {
          setErrorMessages([e.message])
          setIserror(true)
        }
      })
  }, [])

  const handleRowUpdate = (newData: ModelItem, oldData: ModelItem | undefined) => {
    // validation
    const errorList = []
    if (newData.task_name === '') {
      errorList.push('Please enter task name')
    }
    if (newData.scheduled_at === '') {
      errorList.push('Please enter scheduled at')
    }

    if (errorList.length < 1) {
      api
        .patch(`/api/timer-manager/${newData.id}`, newData)
        .then((response) => {
          //   const dataUpdate = [...data]
          //   const index = oldData.id
          //   dataUpdate[index] = newData
          //   setData([...dataUpdate])
          //   setIserror(false)
          //   setErrorMessages([])
        })
        .catch((e: unknown) => {
          if (e instanceof Error) {
            setErrorMessages([e.message])
            setIserror(true)
          }
        })
    } else {
      setErrorMessages(errorList)
      setIserror(true)
    }
  }

  const handleRowAdd = (newData: ModelItem) => {
    // 検証
    const errorList = []
    if (newData.task_name === undefined) {
      errorList.push('コンテンツ名を入力してください')
    }
    if (newData.scheduled_at === undefined) {
      errorList.push('通知時刻を入力してください')
    }
    if (errorList.length < 1) {
      // エラー
      api
        .post('/api/timer-manager', newData)
        .then((res) => {
          const dataToAdd = [...data]
          dataToAdd.push(newData)
          setData(dataToAdd)
          setErrorMessages([])
          setIserror(false)
        })
        .catch((e: unknown) => {
          if (e instanceof Error) {
            setErrorMessages([e.message])
            setIserror(true)
          }
        })
    } else {
      setErrorMessages(errorList)
      setIserror(true)
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
        icons={tableIcons}
        editable={{
          onRowAdd: (newData: ModelItem) =>
            new Promise((resolve) => {
              handleRowAdd(newData)
            }),
          onRowUpdate: (newData: ModelItem, oldData: ModelItem | undefined) =>
            new Promise((resolve) => {
              handleRowUpdate(newData, oldData)
            }),
          //   onRowDelete: (oldData: Model) =>
          //     new Promise((resolve) => {
          //       handleRowDelete(oldData)
          //     }),
        }}
      />
    </div>
  )
}

export default App
