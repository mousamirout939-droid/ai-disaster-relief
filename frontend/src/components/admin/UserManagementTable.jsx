import { useEffect, useState } from 'react'
import axiosClient from '../../api/axiosClient.js'
import Loader from '../common/Loader.jsx'
import { notify } from '../common/Toast.jsx'

export default function UserManagementTable() {
  const [users, setUsers] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  const load = () => {
    setIsLoading(true)
    axiosClient.get('/users').then(({ data }) => {
      setUsers(data.items)
      setIsLoading(false)
    })
  }

  useEffect(load, [])

  const toggleSuspend = async (user) => {
    try {
      await axiosClient.patch(`/users/${user.id}/admin`, { is_suspended: !user.is_suspended })
      notify.success('User updated.')
      load()
    } catch {
      notify.error('Failed to update user.')
    }
  }

  if (isLoading) return <Loader label="Loading users..." />

  return (
    <table className="w-full text-sm">
      <thead>
        <tr className="text-left text-slate-500">
          <th className="pb-2">Name</th>
          <th className="pb-2">Email</th>
          <th className="pb-2">Role</th>
          <th className="pb-2">Status</th>
          <th className="pb-2">Actions</th>
        </tr>
      </thead>
      <tbody>
        {users.map((user) => (
          <tr key={user.id} className="border-t border-slate-100">
            <td className="py-2">{user.full_name}</td>
            <td className="py-2">{user.email}</td>
            <td className="py-2 capitalize">{user.role}</td>
            <td className="py-2">{user.is_suspended ? 'Suspended' : 'Active'}</td>
            <td className="py-2">
              <button onClick={() => toggleSuspend(user)} className="text-brand-700 hover:underline">
                {user.is_suspended ? 'Reinstate' : 'Suspend'}
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
