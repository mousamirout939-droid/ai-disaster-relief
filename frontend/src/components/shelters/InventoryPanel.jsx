import { useEffect, useState } from 'react'
import { inventoryApi } from '../../api/inventoryApi.js'
import Loader from '../common/Loader.jsx'

export default function InventoryPanel({ shelterId }) {
  const [items, setItems] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    inventoryApi.get(shelterId).then(({ data }) => {
      setItems(data)
      setIsLoading(false)
    })
  }, [shelterId])

  if (isLoading) return <Loader label="Loading inventory..." />

  return (
    <table className="w-full text-sm">
      <thead>
        <tr className="text-left text-slate-500">
          <th className="pb-2">Item</th>
          <th className="pb-2">Category</th>
          <th className="pb-2">Quantity</th>
          <th className="pb-2">Status</th>
        </tr>
      </thead>
      <tbody>
        {items.map((item) => (
          <tr key={item.id} className="border-t border-slate-100">
            <td className="py-2">{item.item_name}</td>
            <td className="py-2 capitalize">{item.category}</td>
            <td className="py-2">{item.quantity_available} {item.unit}</td>
            <td className="py-2">
              {item.is_low_stock ? <span className="text-red-600 font-medium">Low stock</span> : <span className="text-green-600">OK</span>}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
