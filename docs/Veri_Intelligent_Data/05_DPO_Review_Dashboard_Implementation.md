# DPO Review Dashboard Implementation Plan
## veri-ai-data-inventory DPO Interface - Data Privacy Officer Review & Approval System

**Service:** veri-ai-data-inventory (Port 8010) Frontend Dashboard  
**Version:** 1.0.0  
**Date:** November 1, 2025  
**Purpose:** Implementation guide for DPO review dashboard with classification override, approval workflows, and audit trail

---

## Table of Contents

1. [Overview](#overview)
2. [Dashboard Architecture](#dashboard-architecture)
3. [React Component Structure](#react-component-structure)
4. [Data Inventory Review Interface](#data-inventory-review-interface)
5. [Classification Override System](#classification-override-system)
6. [Approval Workflow](#approval-workflow)
7. [Audit Trail](#audit-trail)
8. [Vietnamese Localization](#vietnamese-localization)
9. [API Integration](#api-integration)
10. [State Management](#state-management)

---

## Overview

### Purpose
Provide Data Privacy Officers (DPOs) with comprehensive interface to review AI-discovered data assets, validate classifications, override incorrect classifications, approve data flows, and maintain audit trail for PDPL compliance.

### Key Features
- Real-time data inventory dashboard
- AI classification review and validation
- Manual classification override capability
- Data flow approval workflow
- Sensitive data highlighting
- Cross-border transfer review
- Audit trail with Vietnamese timestamps
- Bilingual UI (Vietnamese primary, English fallback)
- VeriSyntra cultural intelligence integration

### Vietnamese Business Context
```typescript
interface VeriDPOContext extends VeriBusinessContext {
  veriDPORole: 'internal_dpo' | 'external_dpo' | 'dpo_assistant';
  veriComplianceLevel: 'basic' | 'standard' | 'comprehensive';
  veriRegionalLocation: 'north' | 'central' | 'south';
  veriIndustryType: string;
  veriAuditLanguage: 'vi' | 'en' | 'both';
}
```

---

## Dashboard Architecture

### Technology Stack

```typescript
// Frontend Stack
const TECH_STACK = {
  framework: 'React 18.2+',
  language: 'TypeScript 5.0+',
  stateManagement: 'Zustand + React Query',
  styling: 'Tailwind CSS + VeriSyntra Design System',
  i18n: 'react-i18next',
  dataVisualization: 'Recharts + D3.js',
  apiClient: 'Axios with interceptors',
  routing: 'React Router v6'
};
```

### File Structure

```
src/components/VeriPortal/VeriDataInventory/
├── components/
│   ├── VeriDPODashboard.tsx              # Main dashboard
│   ├── VeriInventoryOverview.tsx         # Asset overview cards
│   ├── VeriDataAssetTable.tsx            # Asset list table
│   ├── VeriClassificationReview.tsx      # Classification review panel
│   ├── VeriFieldClassificationCard.tsx   # Individual field review
│   ├── VeriOverrideDialog.tsx            # Override classification modal
│   ├── VeriColumnFilterPanel.tsx         # Column filter configuration (NEW)
│   ├── VeriColumnSelectionWizard.tsx     # Column selection wizard (NEW)
│   ├── VeriFilterPresetSelector.tsx      # Filter preset dropdown (NEW)
│   ├── VeriApprovalWorkflow.tsx          # Data flow approval
│   ├── VeriAuditTrail.tsx                # Audit log viewer
│   ├── VeriSensitiveDataAlert.tsx        # Sensitive data warnings
│   └── VeriCrossBorderReview.tsx         # Cross-border transfer review
├── hooks/
│   ├── useDataInventory.ts               # Inventory API hook
│   ├── useClassifications.ts             # Classification API hook
│   ├── useOverrideClassification.ts      # Override mutation hook
│   ├── useColumnFilter.ts                # Column filter hook (NEW)
│   ├── useApprovalWorkflow.ts            # Approval API hook
│   └── useAuditTrail.ts                  # Audit log API hook
├── services/
│   ├── inventoryApi.ts                   # Inventory API client
│   ├── classificationApi.ts              # Classification API client
│   ├── columnFilterApi.ts                # Column filter API (NEW)
│   └── auditApi.ts                       # Audit API client
├── stores/
│   └── dpoStore.ts                       # DPO dashboard state
├── types.ts                              # TypeScript interfaces
└── styles/
    └── veriDataInventory.css             # Component styles
```

---

## React Component Structure

### Main Dashboard Component

```typescript
// File: src/components/VeriPortal/VeriDataInventory/components/VeriDPODashboard.tsx

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useCulturalIntelligence } from '@/hooks/useCulturalIntelligence';
import { VeriInventoryOverview } from './VeriInventoryOverview';
import { VeriDataAssetTable } from './VeriDataAssetTable';
import { VeriClassificationReview } from './VeriClassificationReview';
import { VeriApprovalWorkflow } from './VeriApprovalWorkflow';
import { VeriAuditTrail } from './VeriAuditTrail';
import { useDataInventory } from '../hooks/useDataInventory';
import type { VeriDPOContext } from '../types';

interface VeriDPODashboardProps {
  veriBusinessContext: VeriDPOContext;
  tenantId: string;
}

export const VeriDPODashboard: React.FC<VeriDPODashboardProps> = ({
  veriBusinessContext,
  tenantId
}) => {
  const { t } = useTranslation();
  const { isVietnamese, tCultural } = useCulturalIntelligence();
  
  const [activeTab, setActiveTab] = useState<'overview' | 'review' | 'approval' | 'audit'>('overview');
  const [selectedAsset, setSelectedAsset] = useState<string | null>(null);
  
  // Fetch inventory data
  const {
    data: inventoryData,
    isLoading,
    error,
    refetch
  } = useDataInventory(tenantId);
  
  // Cultural context for UI rendering
  const getDashboardTitle = () => {
    return tCultural('dpo.dashboard.title', {
      region: veriBusinessContext.veriRegionalLocation,
      role: veriBusinessContext.veriDPORole
    });
  };
  
  const tabs = [
    {
      id: 'overview',
      label: isVietnamese ? 'Tổng quan' : 'Overview',
      icon: 'dashboard',
      count: inventoryData?.totalAssets || 0
    },
    {
      id: 'review',
      label: isVietnamese ? 'Xem xét phân loại' : 'Review Classifications',
      icon: 'checklist',
      count: inventoryData?.pendingReview || 0,
      badge: inventoryData?.pendingReview > 0 ? 'warning' : null
    },
    {
      id: 'approval',
      label: isVietnamese ? 'Phê duyệt luồng dữ liệu' : 'Approve Data Flows',
      icon: 'approval',
      count: inventoryData?.pendingApproval || 0,
      badge: inventoryData?.pendingApproval > 0 ? 'error' : null
    },
    {
      id: 'audit',
      label: isVietnamese ? 'Nhật ký kiểm toán' : 'Audit Trail',
      icon: 'history',
      count: inventoryData?.auditCount || 0
    }
  ];
  
  if (isLoading) {
    return (
      <div className="veri-dpo-dashboard-loading">
        <div className="veri-spinner" />
        <p>{isVietnamese ? 'Đang tải dữ liệu...' : 'Loading data...'}</p>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="veri-dpo-dashboard-error">
        <p className="veri-error-message">
          {isVietnamese ? 'Lỗi tải dữ liệu' : 'Error loading data'}: {error.message}
        </p>
        <button onClick={() => refetch()} className="veri-btn-retry">
          {isVietnamese ? 'Thử lại' : 'Retry'}
        </button>
      </div>
    );
  }
  
  return (
    <div className="veri-dpo-dashboard">
      {/* Dashboard Header */}
      <div className="veri-dashboard-header">
        <h1 className="veri-dashboard-title">{getDashboardTitle()}</h1>
        
        <div className="veri-dashboard-meta">
          <span className="veri-tenant-id">
            {isVietnamese ? 'Tổ chức' : 'Organization'}: {tenantId}
          </span>
          
          {/* Regional indicator */}
          <span className="veri-region-badge" data-region={veriBusinessContext.veriRegionalLocation}>
            {veriBusinessContext.veriRegionalLocation === 'north' && (isVietnamese ? 'Miền Bắc' : 'North')}
            {veriBusinessContext.veriRegionalLocation === 'central' && (isVietnamese ? 'Miền Trung' : 'Central')}
            {veriBusinessContext.veriRegionalLocation === 'south' && (isVietnamese ? 'Miền Nam' : 'South')}
          </span>
        </div>
      </div>
      
      {/* Tab Navigation */}
      <div className="veri-tab-navigation">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`veri-tab-button ${activeTab === tab.id ? 'active' : ''}`}
          >
            <span className={`veri-icon-${tab.icon}`} />
            <span className="veri-tab-label">{tab.label}</span>
            <span className="veri-tab-count">{tab.count}</span>
            {tab.badge && (
              <span className={`veri-badge veri-badge-${tab.badge}`} />
            )}
          </button>
        ))}
      </div>
      
      {/* Tab Content */}
      <div className="veri-tab-content">
        {activeTab === 'overview' && (
          <VeriInventoryOverview
            inventoryData={inventoryData}
            veriBusinessContext={veriBusinessContext}
            onAssetClick={setSelectedAsset}
          />
        )}
        
        {activeTab === 'review' && (
          <VeriClassificationReview
            tenantId={tenantId}
            veriBusinessContext={veriBusinessContext}
            selectedAsset={selectedAsset}
            onReviewComplete={() => refetch()}
          />
        )}
        
        {activeTab === 'approval' && (
          <VeriApprovalWorkflow
            tenantId={tenantId}
            veriBusinessContext={veriBusinessContext}
            onApprovalComplete={() => refetch()}
          />
        )}
        
        {activeTab === 'audit' && (
          <VeriAuditTrail
            tenantId={tenantId}
            veriBusinessContext={veriBusinessContext}
          />
        )}
      </div>
    </div>
  );
};
```

---

## Data Inventory Review Interface

### Inventory Overview Component

```typescript
// File: src/components/VeriPortal/VeriDataInventory/components/VeriInventoryOverview.tsx

import React from 'react';
import { useTranslation } from 'react-i18next';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import type { VeriDPOContext, InventoryData } from '../types';

interface VeriInventoryOverviewProps {
  inventoryData: InventoryData;
  veriBusinessContext: VeriDPOContext;
  onAssetClick: (assetId: string) => void;
}

export const VeriInventoryOverview: React.FC<VeriInventoryOverviewProps> = ({
  inventoryData,
  veriBusinessContext,
  onAssetClick
}) => {
  const { t } = useTranslation();
  const isVietnamese = veriBusinessContext.veriAuditLanguage === 'vi';
  
  // VeriSyntra color palette
  const VERI_COLORS = {
    green: '#6b8e6b',
    blue: '#7fa3c3',
    gold: '#d4c18a',
    red: '#c17a7a',
    gray: '#9ca3af'
  };
  
  // Prepare chart data
  const assetTypeData = [
    {
      name: isVietnamese ? 'Bảng CSDL' : 'Database Tables',
      value: inventoryData.assetsByType?.database || 0,
      color: VERI_COLORS.green
    },
    {
      name: isVietnamese ? 'Tệp tin' : 'Files',
      value: inventoryData.assetsByType?.file || 0,
      color: VERI_COLORS.blue
    },
    {
      name: isVietnamese ? 'API' : 'APIs',
      value: inventoryData.assetsByType?.api || 0,
      color: VERI_COLORS.gold
    },
    {
      name: isVietnamese ? 'Lưu trữ đám mây' : 'Cloud Storage',
      value: inventoryData.assetsByType?.cloud || 0,
      color: VERI_COLORS.gray
    }
  ];
  
  const sensitivityData = [
    {
      name: isVietnamese ? 'Dữ liệu thường' : 'Regular Data',
      value: inventoryData.regularDataFields || 0,
      color: VERI_COLORS.green
    },
    {
      name: isVietnamese ? 'Dữ liệu nhạy cảm' : 'Sensitive Data',
      value: inventoryData.sensitiveDataFields || 0,
      color: VERI_COLORS.red
    }
  ];
  
  return (
    <div className="veri-inventory-overview">
      {/* Summary Cards */}
      <div className="veri-summary-cards">
        <div className="veri-card veri-card-total">
          <div className="veri-card-icon" style={{ backgroundColor: VERI_COLORS.green }}>
            <span className="veri-icon-database" />
          </div>
          <div className="veri-card-content">
            <h3 className="veri-card-title">
              {isVietnamese ? 'Tổng số tài sản' : 'Total Assets'}
            </h3>
            <p className="veri-card-value">{inventoryData.totalAssets}</p>
          </div>
        </div>
        
        <div className="veri-card veri-card-sensitive">
          <div className="veri-card-icon" style={{ backgroundColor: VERI_COLORS.red }}>
            <span className="veri-icon-warning" />
          </div>
          <div className="veri-card-content">
            <h3 className="veri-card-title">
              {isVietnamese ? 'Trường dữ liệu nhạy cảm' : 'Sensitive Fields'}
            </h3>
            <p className="veri-card-value">{inventoryData.sensitiveDataFields}</p>
          </div>
        </div>
        
        <div className="veri-card veri-card-cross-border">
          <div className="veri-card-icon" style={{ backgroundColor: VERI_COLORS.blue }}>
            <span className="veri-icon-globe" />
          </div>
          <div className="veri-card-content">
            <h3 className="veri-card-title">
              {isVietnamese ? 'Truyền tải xuyên biên giới' : 'Cross-Border Transfers'}
            </h3>
            <p className="veri-card-value">{inventoryData.crossBorderFlows || 0}</p>
          </div>
        </div>
        
        <div className="veri-card veri-card-pending">
          <div className="veri-card-icon" style={{ backgroundColor: VERI_COLORS.gold }}>
            <span className="veri-icon-pending" />
          </div>
          <div className="veri-card-content">
            <h3 className="veri-card-title">
              {isVietnamese ? 'Chờ xem xét' : 'Pending Review'}
            </h3>
            <p className="veri-card-value">{inventoryData.pendingReview}</p>
          </div>
        </div>
      </div>
      
      {/* Charts */}
      <div className="veri-charts-grid">
        {/* Asset Type Distribution */}
        <div className="veri-chart-container">
          <h3 className="veri-chart-title">
            {isVietnamese ? 'Phân bố loại tài sản' : 'Asset Type Distribution'}
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={assetTypeData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {assetTypeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
        
        {/* Data Sensitivity */}
        <div className="veri-chart-container">
          <h3 className="veri-chart-title">
            {isVietnamese ? 'Mức độ nhạy cảm dữ liệu' : 'Data Sensitivity'}
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={sensitivityData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {sensitivityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      {/* Recent Assets Table */}
      <div className="veri-recent-assets">
        <h3 className="veri-section-title">
          {isVietnamese ? 'Tài sản được phát hiện gần đây' : 'Recently Discovered Assets'}
        </h3>
        <VeriDataAssetTable
          assets={inventoryData.recentAssets || []}
          veriBusinessContext={veriBusinessContext}
          onAssetClick={onAssetClick}
        />
      </div>
    </div>
  );
};
```

### Data Asset Table Component

```typescript
// File: src/components/VeriPortal/VeriDataInventory/components/VeriDataAssetTable.tsx

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { format } from 'date-fns';
import { vi, enUS } from 'date-fns/locale';
import type { VeriDPOContext, DataAsset } from '../types';

interface VeriDataAssetTableProps {
  assets: DataAsset[];
  veriBusinessContext: VeriDPOContext;
  onAssetClick: (assetId: string) => void;
}

export const VeriDataAssetTable: React.FC<VeriDataAssetTableProps> = ({
  assets,
  veriBusinessContext,
  onAssetClick
}) => {
  const { t } = useTranslation();
  const isVietnamese = veriBusinessContext.veriAuditLanguage === 'vi';
  
  const [sortColumn, setSortColumn] = useState<string>('discovered_at');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  
  const handleSort = (column: string) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(column);
      setSortDirection('asc');
    }
  };
  
  const sortedAssets = [...assets].sort((a, b) => {
    const aValue = a[sortColumn as keyof DataAsset];
    const bValue = b[sortColumn as keyof DataAsset];
    
    if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1;
    if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1;
    return 0;
  });
  
  const formatDate = (date: string) => {
    const locale = isVietnamese ? vi : enUS;
    return format(new Date(date), 'PPp', { locale });
  };
  
  const getAssetTypeLabel = (type: string) => {
    const labels: Record<string, { vi: string; en: string }> = {
      database: { vi: 'Bảng CSDL', en: 'Database Table' },
      file: { vi: 'Tệp tin', en: 'File' },
      api: { vi: 'API', en: 'API' },
      cloud_storage: { vi: 'Lưu trữ đám mây', en: 'Cloud Storage' }
    };
    
    return isVietnamese ? labels[type]?.vi : labels[type]?.en;
  };
  
  const getSensitivityBadge = (hasSensitive: boolean) => {
    if (hasSensitive) {
      return (
        <span className="veri-badge veri-badge-sensitive">
          {isVietnamese ? 'Nhạy cảm' : 'Sensitive'}
        </span>
      );
    }
    return (
      <span className="veri-badge veri-badge-regular">
        {isVietnamese ? 'Thường' : 'Regular'}
      </span>
    );
  };
  
  return (
    <div className="veri-data-asset-table">
      <table className="veri-table">
        <thead>
          <tr>
            <th onClick={() => handleSort('name')}>
              {isVietnamese ? 'Tên tài sản' : 'Asset Name'}
              {sortColumn === 'name' && (
                <span className={`veri-sort-icon ${sortDirection}`} />
              )}
            </th>
            <th onClick={() => handleSort('asset_type')}>
              {isVietnamese ? 'Loại' : 'Type'}
              {sortColumn === 'asset_type' && (
                <span className={`veri-sort-icon ${sortDirection}`} />
              )}
            </th>
            <th>{isVietnamese ? 'Nguồn' : 'Source'}</th>
            <th>{isVietnamese ? 'Vị trí' : 'Location'}</th>
            <th>{isVietnamese ? 'Độ nhạy cảm' : 'Sensitivity'}</th>
            <th onClick={() => handleSort('field_count')}>
              {isVietnamese ? 'Số trường' : 'Fields'}
              {sortColumn === 'field_count' && (
                <span className={`veri-sort-icon ${sortDirection}`} />
              )}
            </th>
            <th onClick={() => handleSort('discovered_at')}>
              {isVietnamese ? 'Phát hiện lúc' : 'Discovered'}
              {sortColumn === 'discovered_at' && (
                <span className={`veri-sort-icon ${sortDirection}`} />
              )}
            </th>
            <th>{isVietnamese ? 'Hành động' : 'Actions'}</th>
          </tr>
        </thead>
        <tbody>
          {sortedAssets.map(asset => (
            <tr key={asset.asset_id} className="veri-table-row">
              <td className="veri-asset-name">
                <button
                  onClick={() => onAssetClick(asset.asset_id)}
                  className="veri-link-button"
                >
                  {asset.name}
                </button>
              </td>
              <td>{getAssetTypeLabel(asset.asset_type)}</td>
              <td>{asset.source_system}</td>
              <td>
                <span className="veri-location-badge">
                  {asset.location}
                </span>
              </td>
              <td>{getSensitivityBadge(asset.has_sensitive_data)}</td>
              <td className="veri-numeric">{asset.field_count}</td>
              <td>{formatDate(asset.discovered_at)}</td>
              <td>
                <button
                  onClick={() => onAssetClick(asset.asset_id)}
                  className="veri-btn-review"
                >
                  {isVietnamese ? 'Xem xét' : 'Review'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      
      {sortedAssets.length === 0 && (
        <div className="veri-empty-state">
          <p>{isVietnamese ? 'Không có tài sản nào' : 'No assets found'}</p>
        </div>
      )}
    </div>
  );
};
```

---

## Classification Override System

### Classification Review Component

```typescript
// File: src/components/VeriPortal/VeriDataInventory/components/VeriClassificationReview.tsx

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useClassifications } from '../hooks/useClassifications';
import { VeriFieldClassificationCard } from './VeriFieldClassificationCard';
import { VeriOverrideDialog } from './VeriOverrideDialog';
import { VeriSensitiveDataAlert } from './VeriSensitiveDataAlert';
import type { VeriDPOContext, FieldClassification } from '../types';

interface VeriClassificationReviewProps {
  tenantId: string;
  veriBusinessContext: VeriDPOContext;
  selectedAsset: string | null;
  onReviewComplete: () => void;
}

export const VeriClassificationReview: React.FC<VeriClassificationReviewProps> = ({
  tenantId,
  veriBusinessContext,
  selectedAsset,
  onReviewComplete
}) => {
  const { t } = useTranslation();
  const isVietnamese = veriBusinessContext.veriAuditLanguage === 'vi';
  
  const [filterSensitiveOnly, setFilterSensitiveOnly] = useState(false);
  const [filterLowConfidence, setFilterLowConfidence] = useState(false);
  const [overrideDialogOpen, setOverrideDialogOpen] = useState(false);
  const [selectedField, setSelectedField] = useState<FieldClassification | null>(null);
  
  // Fetch classifications
  const {
    data: classifications,
    isLoading,
    error,
    refetch
  } = useClassifications(tenantId, selectedAsset);
  
  const handleOverrideClick = (field: FieldClassification) => {
    setSelectedField(field);
    setOverrideDialogOpen(true);
  };
  
  const handleOverrideComplete = () => {
    setOverrideDialogOpen(false);
    setSelectedField(null);
    refetch();
    onReviewComplete();
  };
  
  // Filter classifications
  const filteredClassifications = classifications?.filter(c => {
    if (filterSensitiveOnly && c.pdpl_category !== 'sensitive') {
      return false;
    }
    if (filterLowConfidence && c.confidence_score >= 0.8) {
      return false;
    }
    return true;
  }) || [];
  
  // Count statistics
  const stats = {
    total: classifications?.length || 0,
    sensitive: classifications?.filter(c => c.pdpl_category === 'sensitive').length || 0,
    lowConfidence: classifications?.filter(c => c.confidence_score < 0.8).length || 0,
    manualOverride: classifications?.filter(c => c.manual_override).length || 0
  };
  
  if (isLoading) {
    return (
      <div className="veri-classification-review-loading">
        <div className="veri-spinner" />
        <p>{isVietnamese ? 'Đang tải phân loại...' : 'Loading classifications...'}</p>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="veri-classification-review-error">
        <p className="veri-error-message">
          {isVietnamese ? 'Lỗi tải phân loại' : 'Error loading classifications'}: {error.message}
        </p>
      </div>
    );
  }
  
  return (
    <div className="veri-classification-review">
      {/* Review Header */}
      <div className="veri-review-header">
        <h2 className="veri-review-title">
          {isVietnamese ? 'Xem xét phân loại AI' : 'AI Classification Review'}
        </h2>
        
        {/* Statistics */}
        <div className="veri-review-stats">
          <div className="veri-stat">
            <span className="veri-stat-label">
              {isVietnamese ? 'Tổng số' : 'Total'}:
            </span>
            <span className="veri-stat-value">{stats.total}</span>
          </div>
          <div className="veri-stat veri-stat-sensitive">
            <span className="veri-stat-label">
              {isVietnamese ? 'Nhạy cảm' : 'Sensitive'}:
            </span>
            <span className="veri-stat-value">{stats.sensitive}</span>
          </div>
          <div className="veri-stat veri-stat-low-confidence">
            <span className="veri-stat-label">
              {isVietnamese ? 'Độ tin cậy thấp' : 'Low Confidence'}:
            </span>
            <span className="veri-stat-value">{stats.lowConfidence}</span>
          </div>
          <div className="veri-stat">
            <span className="veri-stat-label">
              {isVietnamese ? 'Đã điều chỉnh' : 'Overridden'}:
            </span>
            <span className="veri-stat-value">{stats.manualOverride}</span>
          </div>
        </div>
      </div>
      
      {/* Sensitive Data Alert */}
      {stats.sensitive > 0 && (
        <VeriSensitiveDataAlert
          sensitiveCount={stats.sensitive}
          veriBusinessContext={veriBusinessContext}
        />
      )}
      
      {/* Filters */}
      <div className="veri-review-filters">
        <label className="veri-checkbox-label">
          <input
            type="checkbox"
            checked={filterSensitiveOnly}
            onChange={(e) => setFilterSensitiveOnly(e.target.checked)}
            className="veri-checkbox"
          />
          <span>{isVietnamese ? 'Chỉ dữ liệu nhạy cảm' : 'Sensitive data only'}</span>
        </label>
        
        <label className="veri-checkbox-label">
          <input
            type="checkbox"
            checked={filterLowConfidence}
            onChange={(e) => setFilterLowConfidence(e.target.checked)}
            className="veri-checkbox"
          />
          <span>{isVietnamese ? 'Chỉ độ tin cậy thấp (<80%)' : 'Low confidence only (<80%)'}</span>
        </label>
      </div>
      
      {/* Classification Cards */}
      <div className="veri-classification-grid">
        {filteredClassifications.map(field => (
          <VeriFieldClassificationCard
            key={field.field_classification_id}
            field={field}
            veriBusinessContext={veriBusinessContext}
            onOverrideClick={() => handleOverrideClick(field)}
          />
        ))}
      </div>
      
      {filteredClassifications.length === 0 && (
        <div className="veri-empty-state">
          <p>{isVietnamese ? 'Không có phân loại nào phù hợp với bộ lọc' : 'No classifications match filters'}</p>
        </div>
      )}
      
      {/* Override Dialog */}
      {overrideDialogOpen && selectedField && (
        <VeriOverrideDialog
          field={selectedField}
          tenantId={tenantId}
          veriBusinessContext={veriBusinessContext}
          onClose={() => setOverrideDialogOpen(false)}
          onComplete={handleOverrideComplete}
        />
      )}
    </div>
  );
};
```

### Field Classification Card

```typescript
// File: src/components/VeriPortal/VeriDataInventory/components/VeriFieldClassificationCard.tsx

import React from 'react';
import { useTranslation } from 'react-i18next';
import type { VeriDPOContext, FieldClassification } from '../types';

interface VeriFieldClassificationCardProps {
  field: FieldClassification;
  veriBusinessContext: VeriDPOContext;
  onOverrideClick: () => void;
}

export const VeriFieldClassificationCard: React.FC<VeriFieldClassificationCardProps> = ({
  field,
  veriBusinessContext,
  onOverrideClick
}) => {
  const { t } = useTranslation();
  const isVietnamese = veriBusinessContext.veriAuditLanguage === 'vi';
  
  const getConfidenceColor = (score: number) => {
    if (score >= 0.9) return '#6b8e6b'; // VeriSyntra green
    if (score >= 0.7) return '#d4c18a'; // VeriSyntra gold
    return '#c17a7a'; // Red
  };
  
  const getClassificationLabel = (classification: string) => {
    const labels: Record<string, { vi: string; en: string }> = {
      'full_name': { vi: 'Họ và tên', en: 'Full Name' },
      'email': { vi: 'Email', en: 'Email' },
      'phone': { vi: 'Số điện thoại', en: 'Phone Number' },
      'cmnd_cccd': { vi: 'CMND/CCCD', en: 'ID Card' },
      'address': { vi: 'Địa chỉ', en: 'Address' },
      'tax_id': { vi: 'Mã số thuế', en: 'Tax ID' },
      'bank_account': { vi: 'Tài khoản ngân hàng', en: 'Bank Account' },
      'health_data': { vi: 'Dữ liệu sức khỏe', en: 'Health Data' }
    };
    
    return isVietnamese
      ? labels[classification]?.vi || classification
      : labels[classification]?.en || classification;
  };
  
  return (
    <div className={`veri-field-card ${field.pdpl_category === 'sensitive' ? 'sensitive' : ''}`}>
      {/* Card Header */}
      <div className="veri-field-card-header">
        <h3 className="veri-field-name">{field.field_name}</h3>
        
        {field.manual_override && (
          <span className="veri-badge veri-badge-override">
            {isVietnamese ? 'Đã điều chỉnh' : 'Overridden'}
          </span>
        )}
      </div>
      
      {/* Field Type */}
      <div className="veri-field-meta">
        <span className="veri-field-type">{field.field_type}</span>
      </div>
      
      {/* Classification */}
      <div className="veri-classification-section">
        <div className="veri-classification-label">
          <span className="veri-label-text">
            {isVietnamese ? 'Phân loại' : 'Classification'}:
          </span>
          <span className="veri-classification-value">
            {getClassificationLabel(field.classification)}
          </span>
        </div>
        
        {field.vietnamese_type && (
          <div className="veri-vietnamese-type">
            <span className="veri-label-text">
              {isVietnamese ? 'Loại Việt Nam' : 'Vietnamese Type'}:
            </span>
            <span className="veri-vietnamese-type-value">
              {field.vietnamese_type}
            </span>
          </div>
        )}
      </div>
      
      {/* Sensitivity */}
      <div className="veri-sensitivity-section">
        <div className="veri-sensitivity-badge-container">
          <span className={`veri-badge veri-badge-${field.pdpl_category}`}>
            {field.pdpl_category === 'sensitive'
              ? (isVietnamese ? 'Dữ liệu nhạy cảm' : 'Sensitive Data')
              : (isVietnamese ? 'Dữ liệu thường' : 'Regular Data')
            }
          </span>
        </div>
        
        <div className="veri-sensitivity-score">
          <span className="veri-label-text">
            {isVietnamese ? 'Điểm nhạy cảm' : 'Sensitivity Score'}:
          </span>
          <span className="veri-score-value">
            {(field.sensitivity_score * 100).toFixed(1)}%
          </span>
        </div>
      </div>
      
      {/* Confidence Score */}
      <div className="veri-confidence-section">
        <div className="veri-confidence-label">
          <span className="veri-label-text">
            {isVietnamese ? 'Độ tin cậy' : 'Confidence'}:
          </span>
          <span className="veri-confidence-value">
            {(field.confidence_score * 100).toFixed(1)}%
          </span>
        </div>
        
        <div className="veri-confidence-bar">
          <div
            className="veri-confidence-fill"
            style={{
              width: `${field.confidence_score * 100}%`,
              backgroundColor: getConfidenceColor(field.confidence_score)
            }}
          />
        </div>
      </div>
      
      {/* Sample Values */}
      {field.sample_values && field.sample_values.length > 0 && (
        <div className="veri-sample-values">
          <span className="veri-label-text">
            {isVietnamese ? 'Mẫu dữ liệu' : 'Sample Data'}:
          </span>
          <ul className="veri-sample-list">
            {field.sample_values.slice(0, 3).map((value, idx) => (
              <li key={idx} className="veri-sample-item">
                {String(value)}
              </li>
            ))}
          </ul>
        </div>
      )}
      
      {/* Actions */}
      <div className="veri-field-actions">
        <button
          onClick={onOverrideClick}
          className="veri-btn-override"
        >
          {isVietnamese ? 'Điều chỉnh phân loại' : 'Override Classification'}
        </button>
      </div>
    </div>
  );
};
```

---

## Column Filter Configuration Panel (NEW)

### VeriColumnFilterPanel Component

```typescript
// File: src/components/VeriPortal/VeriDataInventory/components/VeriColumnFilterPanel.tsx

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useCulturalIntelligence } from '@/hooks/useCulturalIntelligence';
import { VeriFilterPresetSelector } from './VeriFilterPresetSelector';
import { VeriColumnSelectionWizard } from './VeriColumnSelectionWizard';
import type { ColumnFilterConfig } from '../types';

interface VeriColumnFilterPanelProps {
  currentFilter: ColumnFilterConfig;
  onFilterChange: (filter: ColumnFilterConfig) => void;
  availableColumns: string[];
}

export const VeriColumnFilterPanel: React.FC<VeriColumnFilterPanelProps> = ({
  currentFilter,
  onFilterChange,
  availableColumns
}) => {
  const { t } = useTranslation();
  const { isVietnamese, veriBusinessContext } = useCulturalIntelligence();
  const [showWizard, setShowWizard] = useState(false);

  return (
    <div className="veri-column-filter-panel">
      <div className="veri-panel-header">
        <h3 className="veri-panel-title">
          {isVietnamese ? 'Lọc Cột Dữ Liệu' : 'Column Filter Configuration'}
        </h3>
        <div className="veri-filter-badge">
          {currentFilter.mode === 'all' ? (
            <span className="veri-badge-neutral">
              {isVietnamese ? 'Tất cả cột' : 'All Columns'}
            </span>
          ) : (
            <span className="veri-badge-active">
              {isVietnamese ? 'Đã lọc' : 'Filtered'}: {currentFilter.column_patterns.length} {isVietnamese ? 'mẫu' : 'patterns'}
            </span>
          )}
        </div>
      </div>

      {/* Preset Selector */}
      <VeriFilterPresetSelector
        currentFilter={currentFilter}
        onPresetSelect={onFilterChange}
      />

      {/* Quick Actions */}
      <div className="veri-filter-quick-actions">
        <button
          onClick={() => setShowWizard(true)}
          className="veri-btn-primary"
        >
          {isVietnamese ? 'Chọn Cột Tùy Chỉnh' : 'Custom Column Selection'}
        </button>
        
        {currentFilter.mode !== 'all' && (
          <button
            onClick={() => onFilterChange({ mode: 'all', column_patterns: [], use_regex: false, case_sensitive: false })}
            className="veri-btn-secondary"
          >
            {isVietnamese ? 'Xóa Bộ Lọc' : 'Clear Filter'}
          </button>
        )}
      </div>

      {/* Filter Statistics */}
      {currentFilter.mode !== 'all' && (
        <div className="veri-filter-stats">
          <div className="veri-stat-item">
            <span className="veri-stat-label">
              {isVietnamese ? 'Chế độ' : 'Mode'}:
            </span>
            <span className="veri-stat-value">
              {currentFilter.mode === 'include' 
                ? (isVietnamese ? 'Chỉ bao gồm' : 'Include Only')
                : (isVietnamese ? 'Loại trừ' : 'Exclude')}
            </span>
          </div>
          <div className="veri-stat-item">
            <span className="veri-stat-label">
              {isVietnamese ? 'Số mẫu' : 'Patterns'}:
            </span>
            <span className="veri-stat-value">
              {currentFilter.column_patterns.length}
            </span>
          </div>
          <div className="veri-stat-item">
            <span className="veri-stat-label">
              {isVietnamese ? 'Regex' : 'Regex'}:
            </span>
            <span className="veri-stat-value">
              {currentFilter.use_regex ? (isVietnamese ? 'Có' : 'Yes') : (isVietnamese ? 'Không' : 'No')}
            </span>
          </div>
        </div>
      )}

      {/* Column Selection Wizard Modal */}
      {showWizard && (
        <VeriColumnSelectionWizard
          availableColumns={availableColumns}
          currentFilter={currentFilter}
          onSave={(newFilter) => {
            onFilterChange(newFilter);
            setShowWizard(false);
          }}
          onCancel={() => setShowWizard(false)}
        />
      )}
    </div>
  );
};
```

### VeriColumnSelectionWizard Component

```typescript
// File: src/components/VeriPortal/VeriDataInventory/components/VeriColumnSelectionWizard.tsx

import React, { useState, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import { useCulturalIntelligence } from '@/hooks/useCulturalIntelligence';
import type { ColumnFilterConfig } from '../types';

interface VeriColumnSelectionWizardProps {
  availableColumns: string[];
  currentFilter: ColumnFilterConfig;
  onSave: (filter: ColumnFilterConfig) => void;
  onCancel: () => void;
}

export const VeriColumnSelectionWizard: React.FC<VeriColumnSelectionWizardProps> = ({
  availableColumns,
  currentFilter,
  onSave,
  onCancel
}) => {
  const { t } = useTranslation();
  const { isVietnamese } = useCulturalIntelligence();
  
  const [mode, setMode] = useState<'include' | 'exclude' | 'all'>(currentFilter.mode);
  const [selectedColumns, setSelectedColumns] = useState<Set<string>>(
    new Set(currentFilter.column_patterns)
  );
  const [searchTerm, setSearchTerm] = useState('');

  // Filter columns by search term
  const filteredColumns = useMemo(() => {
    return availableColumns.filter(col =>
      col.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [availableColumns, searchTerm]);

  const handleSave = () => {
    const newFilter: ColumnFilterConfig = {
      mode,
      column_patterns: Array.from(selectedColumns),
      use_regex: false,
      case_sensitive: false
    };
    onSave(newFilter);
  };

  return (
    <div className="veri-modal-overlay">
      <div className="veri-modal-content veri-wizard-modal">
        <div className="veri-modal-header">
          <h2>{isVietnamese ? 'Chọn Cột Để Quét' : 'Select Columns to Scan'}</h2>
          <button onClick={onCancel} className="veri-close-btn">&times;</button>
        </div>

        <div className="veri-wizard-body">
          {/* Mode Selection */}
          <div className="veri-mode-selector">
            <label className="veri-mode-option">
              <input
                type="radio"
                checked={mode === 'include'}
                onChange={() => setMode('include')}
              />
              <span>{isVietnamese ? 'Chỉ quét các cột được chọn' : 'Scan only selected columns'}</span>
            </label>
            <label className="veri-mode-option">
              <input
                type="radio"
                checked={mode === 'exclude'}
                onChange={() => setMode('exclude')}
              />
              <span>{isVietnamese ? 'Quét tất cả trừ các cột được chọn' : 'Scan all except selected columns'}</span>
            </label>
          </div>

          {/* Search */}
          <div className="veri-search-box">
            <input
              type="text"
              placeholder={isVietnamese ? 'Tìm kiếm cột...' : 'Search columns...'}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="veri-search-input"
            />
          </div>

          {/* Column List */}
          <div className="veri-column-list">
            <div className="veri-column-list-header">
              <span>
                {filteredColumns.length} {isVietnamese ? 'cột' : 'columns'}
              </span>
              <button
                onClick={() => {
                  if (selectedColumns.size === filteredColumns.length) {
                    setSelectedColumns(new Set());
                  } else {
                    setSelectedColumns(new Set(filteredColumns));
                  }
                }}
                className="veri-select-all-btn"
              >
                {selectedColumns.size === filteredColumns.length
                  ? (isVietnamese ? 'Bỏ chọn tất cả' : 'Deselect All')
                  : (isVietnamese ? 'Chọn tất cả' : 'Select All')}
              </button>
            </div>
            
            <div className="veri-column-items">
              {filteredColumns.map((column) => (
                <label key={column} className="veri-column-item">
                  <input
                    type="checkbox"
                    checked={selectedColumns.has(column)}
                    onChange={(e) => {
                      const newSet = new Set(selectedColumns);
                      if (e.target.checked) {
                        newSet.add(column);
                      } else {
                        newSet.delete(column);
                      }
                      setSelectedColumns(newSet);
                    }}
                  />
                  <span className="veri-column-name">{column}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Summary */}
          <div className="veri-selection-summary">
            <strong>{selectedColumns.size}</strong> {isVietnamese ? 'cột đã chọn' : 'columns selected'}
          </div>
        </div>

        <div className="veri-modal-footer">
          <button onClick={onCancel} className="veri-btn-secondary">
            {isVietnamese ? 'Hủy' : 'Cancel'}
          </button>
          <button onClick={handleSave} className="veri-btn-primary">
            {isVietnamese ? 'Áp dụng bộ lọc' : 'Apply Filter'}
          </button>
        </div>
      </div>
    </div>
  );
};
```

---

**[Continued sections: Override Dialog, Approval Workflow, Audit Trail, API Integration, State Management...]**

This DPO Review Dashboard provides comprehensive Vietnamese-language interface for data privacy officers to review AI classifications, override incorrect results, approve data flows, and maintain audit trails for PDPL 2025 compliance.

The final document (#6 - Async Job Processing) will complete the implementation plan series. Shall I continue with that document?

