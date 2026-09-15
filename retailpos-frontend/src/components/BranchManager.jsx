import React, { useState, useEffect } from 'react';
import client from '../api/client';

export default function BranchManager() {
  const [branches, setBranches] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [form, setForm] = useState({
    BranchCode: '', BranchName: '', MobileNo: '', EmailId: '', GSTNo: '', Address: '', CostCode: 'AUTHORIZED', IsActive: true
  });

  const loadBranches = async () => {
    const res = await client.get('/branches');
    setBranches(res.data);
  };

  useEffect(() => { loadBranches(); }, []);

  const handleSave = async () => {
    if (selectedId) {
      await client.put(`/branches/${selectedId}`, form);
    } else {
      await client.post('/branches', form);
    }
    loadBranches();
    clearForm();
  };

  const handleDelete = async () => {
    if (selectedId) {
      await client.delete(`/branches/${selectedId}`);
      loadBranches();
      clearForm();
    }
  };

  const clearForm = () => {
    setSelectedId(null);
    setForm({ BranchCode: '', BranchName: '', MobileNo: '', EmailId: '', GSTNo: '', Address: '', CostCode: 'AUTHORIZED', IsActive: true });
  };

  return (
    <div className="manager-grid">
      <div className="form-container">
        <h3>Branch Setup</h3>
        <input placeholder="Branch Code" value={form.BranchCode} onChange={e => setForm({...form, BranchCode: e.target.value})} />
        <input placeholder="Branch Name" value={form.BranchName} onChange={e => setForm({...form, BranchName: e.target.value})} />
        <input placeholder="Mobile No" value={form.MobileNo} onChange={e => setForm({...form, MobileNo: e.target.value})} />
        <input placeholder="Email ID" value={form.EmailId} onChange={e => setForm({...form, EmailId: e.target.value})} />
        <input placeholder="GST No" value={form.GSTNo} onChange={e => setForm({...form, GSTNo: e.target.value})} />
        <input placeholder="Address" value={form.Address} onChange={e => setForm({...form, Address: e.target.value})} />
        <input placeholder="Cost Code" value={form.CostCode} onChange={e => setForm({...form, CostCode: e.target.value})} />
        <div className="btn-group">
          <button onClick={handleSave}>{selectedId ? 'Update' : 'Save'}</button>
          {selectedId && <button onClick={handleDelete} className="btn-danger">Delete</button>}
          <button onClick={clearForm}>Clear</button>
        </div>
      </div>
      <div className="table-container">
        <table>
          <thead>
            <tr><th>ID</th><th>Code</th><th>Name</th><th>Mobile</th><th>Status</th></tr>
          </thead>
          <tbody>
            {branches.map(b => (
              <tr key={b.BranchId} onClick={() => { setSelectedId(b.BranchId); setForm(b); }}>
                <td>{b.BranchId}</td>
                <td>{b.BranchCode}</td>
                <td>{b.BranchName}</td>
                <td>{b.MobileNo}</td>
                <td>{b.IsActive ? 'Active' : 'Inactive'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}