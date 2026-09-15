import React, { useState, useEffect } from 'react';
import client from '../api/client';

export default function SlabManager() {
  const [type, setType] = useState('Age Slab');
  const [data, setData] = useState([]);
  const [form, setForm] = useState({
    id: '', name: '', desc: '', from: '', to: '', group: '', set: ''
  });

  const loadData = async () => {
    const endpoint = type === 'Age Slab' ? '/slabs/age' : '/slabs/price';
    const res = await client.get(endpoint);
    setData(res.data);
  };

  useEffect(() => { loadData(); }, [type]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (type === 'Age Slab') {
      await client.post('/slabs/age', {
        AgeSlabId: parseInt(form.id),
        AgeSlabName: form.name,
        AgeSlabDesc: form.desc,
        AgeFrDays: parseInt(form.from),
        AgeToDays: parseInt(form.to),
        IsActive: true
      });
    } else {
      await client.post('/slabs/price', {
        PriceSlabID: parseInt(form.id),
        PriceSlabName: form.name,
        PriceSlabGroup: form.group,
        PriceSlabDesc: form.desc,
        PriceSlabFrAmt: parseFloat(form.from),
        PriceSlabToAmt: parseFloat(form.to),
        PriceSlabSetName: form.set,
        IsActive: true
      });
    }
    loadData();
    clearForm();
  };

  const clearForm = () => {
    setForm({ id: '', name: '', desc: '', from: '', to: '', group: '', set: '' });
  };

  return (
    <div className="manager-grid">
      <div className="form-container">
        <h3>Slab Master</h3>
        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="Age Slab">Age Slab</option>
          <option value="Price Slab">Price Slab</option>
        </select>
        <form onSubmit={handleSubmit}>
          <input placeholder="ID" value={form.id} onChange={(e) => setForm({...form, id: e.target.value})} required />
          <input placeholder="Name" value={form.name} onChange={(e) => setForm({...form, name: e.target.value})} required />
          {type === 'Price Slab' && <input placeholder="Group" value={form.group} onChange={(e) => setForm({...form, group: e.target.value})} />}
          <input placeholder="Description" value={form.desc} onChange={(e) => setForm({...form, desc: e.target.value})} />
          <input placeholder={type === 'Age Slab' ? "From Days" : "From Amount"} value={form.from} onChange={(e) => setForm({...form, from: e.target.value})} required />
          <input placeholder={type === 'Age Slab' ? "To Days" : "To Amount"} value={form.to} onChange={(e) => setForm({...form, to: e.target.value})} required />
          {type === 'Price Slab' && <input placeholder="Set Name" value={form.set} onChange={(e) => setForm({...form, set: e.target.value})} />}
          <div className="btn-group">
            <button type="submit">Save / Add</button>
            <button type="button" onClick={clearForm}>Clear</button>
          </div>
        </form>
      </div>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th><th>Name</th><th>Desc</th><th>From</th><th>To</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row) => (
              <tr key={row.AgeSlabId || row.PriceSlabID}>
                <td>{row.AgeSlabId || row.PriceSlabID}</td>
                <td>{row.AgeSlabName || row.PriceSlabName}</td>
                <td>{row.AgeSlabDesc || row.PriceSlabDesc}</td>
                <td>{row.AgeFrDays ?? row.PriceSlabFrAmt}</td>
                <td>{row.AgeToDays ?? row.PriceSlabToAmt}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}