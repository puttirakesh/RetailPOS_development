import React, { useState, useEffect } from 'react';
import client from '../api/client';

export default function SupplierManager() {
  const [suppliers, setSuppliers] = useState([]);
  const [form, setForm] = useState({
    SupplierId: '', SupplierCode: '', SupplierName: '', MobileNo: '', GSTNo: '', Address: '', OpeningBalance: 0.0, IsActive: true
  });

  const loadSuppliers = async () => {
    const res = await client.get('/suppliers');
    setSuppliers(res.data);
  };

  useEffect(() => { loadSuppliers(); }, []);

  const handleSave = async () => {
    await client.post('/suppliers', { ...form, SupplierId: parseInt(form.SupplierId) });
    loadSuppliers();
    clearForm();
  };

  const handleDelete = async (id) => {
    await client.delete(`/suppliers/${id}`);
    loadSuppliers();
    clearForm();
  };

  const clearForm = () => {
    setForm({ SupplierId: '', SupplierCode: '', SupplierName: '', MobileNo: '', GSTNo: '', Address: '', OpeningBalance: 0.0, IsActive: true });
  };

  return (
    <div className="manager-grid">
      <div className="form-container">
        <h3>Supplier Setup</h3>
        <input placeholder="Supplier ID" value={form.SupplierId} onChange={e => setForm({...form, SupplierId: e.target.value})} />
        <input placeholder="Supplier Name" value={form.SupplierName} onChange={e => setForm({...form, SupplierName: e.target.value, SupplierCode: e.target.value.substring(0,3).toUpperCase()})} />
        <input placeholder="Supplier Code" value={form.SupplierCode} onChange={e => setForm({...form, SupplierCode: e.target.value})} />
        <input placeholder="Mobile No" value={form.MobileNo} onChange={e => setForm({...form, MobileNo: e.target.value})} />
        <input placeholder="GST No" value={form.GSTNo} onChange={e => setForm({...form, GSTNo: e.target.value})} />
        <div className="btn-group">
          <button onClick={handleSave}>Save / Update</button>
          <button onClick={clearForm}>Clear</button>
        </div>
      </div>
      <div className="table-container">
        <table>
          <thead>
            <tr><th>ID</th><th>Code</th><th>Name</th><th>GST No</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {suppliers.map(s => (
              <tr key={s.SupplierId} onClick={() => setForm(s)}>
                <td>{s.SupplierId}</td>
                <td>{s.SupplierCode}</td>
                <td>{s.SupplierName}</td>
                <td>{s.GSTNo}</td>
                <td><button onClick={() => handleDelete(s.SupplierId)} className="btn-danger">Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}