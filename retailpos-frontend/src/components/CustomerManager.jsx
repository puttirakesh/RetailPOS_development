import React, { useState, useEffect } from 'react';
import client from '../api/client';

export default function CustomerManager() {
  const [customers, setCustomers] = useState([]);
  const [form, setForm] = useState({
    CustomerId: '', CustomerCode: '', CustomerName: '', MobileNo: '', EmailId: '', Address: '', OpeningBalance: 0.0, IsActive: true
  });

  const loadCustomers = async () => {
    const res = await client.get('/customers');
    setCustomers(res.data);
  };

  useEffect(() => { loadCustomers(); }, []);

  const handleSave = async () => {
    await client.post('/customers', { ...form, CustomerId: parseInt(form.CustomerId) });
    loadCustomers();
    clearForm();
  };

  const handleDelete = async (id) => {
    await client.delete(`/customers/${id}`);
    loadCustomers();
    clearForm();
  };

  const clearForm = () => {
    setForm({ CustomerId: '', CustomerCode: '', CustomerName: '', MobileNo: '', EmailId: '', Address: '', OpeningBalance: 0.0, IsActive: true });
  };

  return (
    <div className="manager-grid">
      <div className="form-container">
        <h3>Customer Setup</h3>
        <input placeholder="Customer ID" value={form.CustomerId} onChange={e => setForm({...form, CustomerId: e.target.value, CustomerCode: e.target.value})} />
        <input placeholder="Customer Name" value={form.CustomerName} onChange={e => setForm({...form, CustomerName: e.target.value})} />
        <input placeholder="Mobile No" value={form.MobileNo} onChange={e => setForm({...form, MobileNo: e.target.value})} />
        <input placeholder="Email ID" value={form.EmailId} onChange={e => setForm({...form, EmailId: e.target.value})} />
        <textarea placeholder="Address" value={form.Address} onChange={e => setForm({...form, Address: e.target.value})} />
        <div className="btn-group">
          <button onClick={handleSave}>Save / Update</button>
          <button onClick={clearForm}>Clear</button>
        </div>
      </div>
      <div className="table-container">
        <table>
          <thead>
            <tr><th>Code</th><th>Name</th><th>Mobile</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {customers.map(c => (
              <tr key={c.CustomerId} onClick={() => setForm(c)}>
                <td>{c.CustomerCode}</td>
                <td>{c.CustomerName}</td>
                <td>{c.MobileNo}</td>
                <td><button onClick={() => handleDelete(c.CustomerId)} className="btn-danger">Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}