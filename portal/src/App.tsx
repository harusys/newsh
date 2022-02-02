import { VFC, useState, useEffect } from 'react'
import MaterialTable from '@material-table/core'
import axios from 'axios'
import tableIcons from './MaterialTableIcons'

const api = axios.create({
  responseType: 'json',
})

interface ITimerManager {
  id: string
  user_id: string
  task_name: string
  scheduled_at: string
}

const App: VFC = () => {
  const [columns, setColumns] = useState([
    { title: 'ID', field: 'id' },
    { title: 'ユーザID', field: 'user_id', hidden: true },
    { title: 'コンテンツ名', field: 'task_name' },
    { title: '通知時刻', field: 'scheduled_at' },
  ])

  const [data, setData] = useState<Array<ITimerManager>>([])

  // for error handling
  const [iserror, setIserror] = useState(false)
  const [errorMessages, setErrorMessages] = useState<Array<string>>([])

  useEffect(() => {
    api
      .get<Array<ITimerManager>>('/api/timer-manager/Ud9f705bf1ae17b6111b1b5353b00eaf7')
      .then((response) => {
        setData(
          response.data.map<ITimerManager>((d) => ({
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

  const handleRowUpdate = (newData: ITimerManager, oldData: ITimerManager | undefined) => {
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
        .then((res) => {
          //   const dataUpdate = [...data]
          //   const index = oldData.id
          //   dataUpdate[index] = newData
          //   setData([...dataUpdate])
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

  const handleRowAdd = (newData: ITimerManager) => {
    // 検証
    /* eslint-disable */
    newData.user_id = 'xxx'
    console.log(newData)
    /* eslint-enable */
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
          setData([...data, newData])
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
      <MaterialTable
        title="通知設定画面"
        columns={columns}
        data={data}
        icons={tableIcons}
        editable={{
          onRowAdd: (newData: ITimerManager) =>
            new Promise((resolve) => {
              handleRowAdd(newData)
              resolve('OK')
            }),
          onRowUpdate: (newData: ITimerManager, oldData: ITimerManager | undefined) =>
            new Promise((resolve) => {
              handleRowUpdate(newData, oldData)
              resolve('OK')
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
