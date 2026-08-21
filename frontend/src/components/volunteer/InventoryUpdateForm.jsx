import { useForm } from 'react-hook-form'
import { inventoryApi } from '../../api/inventoryApi.js'
import { notify } from '../common/Toast.jsx'
import Button from '../common/Button.jsx'

export default function InventoryUpdateForm({ shelterId, onUpdated }) {
  const { register, handleSubmit, reset, formState: { isSubmitting } } = useForm()

  const onSubmit = async (values) => {
    try {
      await inventoryApi.update(shelterId, {
        category: values.category,
        item_name: values.item_name,
        quantity_available: Number(values.quantity_available),
        unit: values.unit || 'units',
      })
      notify.success('Inventory updated.')
      reset()
      onUpdated?.()
    } catch {
      notify.error('Failed to update inventory.')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="card space-y-3">
      <h3 className="font-semibold">Update Shelter Inventory</h3>
      <select {...register('category', { required: true })} className="input-field">
        <option value="food">Food</option>
        <option value="water">Water</option>
        <option value="medical">Medical</option>
        <option value="bedding">Bedding</option>
        <option value="hygiene">Hygiene</option>
        <option value="clothing">Clothing</option>
        <option value="other">Other</option>
      </select>
      <input {...register('item_name', { required: true })} placeholder="Item name" className="input-field" />
      <div className="flex gap-2">
        <input {...register('quantity_available', { required: true })} type="number" placeholder="Quantity" className="input-field" />
        <input {...register('unit')} placeholder="Unit (e.g. liters, kg)" className="input-field" />
      </div>
      <Button type="submit" disabled={isSubmitting} className="w-full">
        {isSubmitting ? 'Saving...' : 'Update Inventory'}
      </Button>
    </form>
  )
}
