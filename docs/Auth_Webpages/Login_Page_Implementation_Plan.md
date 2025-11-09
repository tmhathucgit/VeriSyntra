# VeriSyntra Login Page - Implementation Plan

**Date:** 2025-11-01  
**Component:** Login Authentication Page  
**Route:** `/login`  
**API Endpoint:** `http://localhost:8001/api/v1/auth/login`  
**Status:** Planning Phase

---

## 1. Overview

### Purpose
Create a bilingual (Vietnamese/English) login page that authenticates users against the PostgreSQL-backed auth service and provides a culturally-appropriate Vietnamese business experience.

### User Flow
```
Landing Page (/) 
  -> Click "Enter App" / "Get Started"
  -> Login Page (/login) [NEW]
  -> Submit credentials
  -> Auth Service validates (PostgreSQL)
  -> Store JWT tokens
  -> Redirect to Dashboard (/app)
```

### Key Requirements
- [X] Bilingual UI (Vietnamese-first with English toggle)
- [X] Integration with existing auth service API (`/api/v1/auth/login`)
- [X] JWT token management (access + refresh tokens)
- [X] Vietnamese business context support
- [X] Form validation with Vietnamese error messages
- [X] Responsive design matching VeriSyntra brand colors
- [X] Remember me functionality
- [X] Forgot password link (future implementation)
- [X] Link to registration page

---

## 2. Technical Architecture

### File Structure
```
src/
├── components/
│   └── Auth/
│       ├── Login/
│       │   ├── LoginPage.tsx           # Main login component
│       │   ├── LoginForm.tsx           # Form component with validation
│       │   ├── types.ts                # TypeScript interfaces
│       │   └── styles.css              # Component-specific styles (optional)
│       └── shared/
│           ├── AuthLayout.tsx          # Shared auth page layout
│           └── LanguageToggle.tsx      # Language switcher for auth pages
├── services/
│   └── auth/
│       ├── authService.ts              # API calls to auth service
│       └── tokenManager.ts             # JWT token storage/retrieval
├── stores/
│   └── authStore.ts                    # Zustand store for auth state
└── locales/
    ├── vi/
    │   └── auth.json                   # Vietnamese translations
    └── en/
        └── auth.json                   # English translations
```

### State Management
```typescript
// authStore.ts (Zustand)
interface AuthState {
  user: VeriUser | null;
  tenant: VeriTenant | null;
  veriBusinessContext: VeriBusinessContext | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  refreshAccessToken: () => Promise<void>;
  setUser: (user: VeriUser) => void;
}
```

---

## 3. API Integration

### Login Endpoint
**URL:** `POST http://localhost:8001/api/v1/auth/login`

**Request Body:**
```typescript
interface VeriUserLogin {
  email: string;              // Required: user@example.com
  password: string;           // Required: min 8 chars
  tenant_id: string;          // Required: UUID of tenant (for multi-tenant support)
}
```

**Success Response (200 OK):**
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "user_id": "uuid",
    "email": "test@verisyntra.vn",
    "full_name": "Nguyen Van Test",
    "tenant_id": "uuid",
    "role": "admin"
  },
  "veri_business_context": {
    "veriBusinessId": "uuid",
    "veriRegionalLocation": "south",
    "veriIndustryType": "technology",
    "veriSubscriptionTier": "starter"
  },
  "message": "Dang nhap thanh cong / Login successful",
  "english": "Login successful",
  "vietnam_time": "2025-11-02T04:45:01.271487+07:00"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": {
    "message": "Email hoac mat khau khong dung / Invalid email or password",
    "english": "Invalid email or password"
  }
}
```

**Error Response (403 Forbidden - Inactive Account):**
```json
{
  "detail": {
    "message": "Tai khoan da bi vo hieu hoa / Account is inactive",
    "english": "Account is inactive"
  }
}
```

### Token Storage Strategy
```typescript
// tokenManager.ts
class TokenManager {
  private readonly ACCESS_TOKEN_KEY = 'veri_access_token';
  private readonly REFRESH_TOKEN_KEY = 'veri_refresh_token';
  private readonly USER_KEY = 'veri_user';
  private readonly BUSINESS_CONTEXT_KEY = 'veri_business_context';

  saveTokens(accessToken: string, refreshToken: string): void {
    localStorage.setItem(this.ACCESS_TOKEN_KEY, accessToken);
    localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
  }

  getAccessToken(): string | null {
    return localStorage.getItem(this.ACCESS_TOKEN_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }

  clearTokens(): void {
    localStorage.removeItem(this.ACCESS_TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    localStorage.removeItem(this.BUSINESS_CONTEXT_KEY);
  }

  saveUser(user: VeriUser): void {
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));
  }

  getUser(): VeriUser | null {
    const user = localStorage.getItem(this.USER_KEY);
    return user ? JSON.parse(user) : null;
  }
}
```

---

## 4. UI/UX Design Specifications

### Vietnamese Color Palette (from copilot-instructions.md)
```css
:root {
  --veri-green: #6b8e6b;      /* Primary - Vietnamese green */
  --veri-blue: #7fa3c3;       /* Secondary - Vietnamese blue */
  --veri-gold: #d4c18a;       /* Accent - Vietnamese gold */
  --veri-error: #c17a7a;      /* Error state */
}
```

### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│  [VN Map Logo]  VeriSyntra                   [🇻🇳 VI ▼] │ <- Header
├─────────────────────────────────────────────────────────┤
│                                                         │
│     ┌──────────────────────────────────────┐          │
│     │                                      │          │
│     │   Chào mừng trở lại / Welcome Back  │          │ <- Title
│     │                                      │          │
│     │   ┌────────────────────────────┐    │          │
│     │   │ Email                       │    │          │ <- Email Input
│     │   │ test@verisyntra.vn          │    │          │
│     │   └────────────────────────────┘    │          │
│     │                                      │          │
│     │   ┌────────────────────────────┐    │          │
│     │   │ Mật khẩu / Password   [👁]  │    │          │ <- Password Input
│     │   │ ••••••••                    │    │          │
│     │   └────────────────────────────┘    │          │
│     │                                      │          │
│     │   [✓] Ghi nhớ đăng nhập              │          │ <- Remember Me
│     │                                      │          │
│     │   ┌────────────────────────────┐    │          │
│     │   │   Đăng nhập / Login        │    │          │ <- Submit Button
│     │   └────────────────────────────┘    │          │
│     │                                      │          │
│     │   Quên mật khẩu? / Forgot Password?  │          │ <- Forgot Link
│     │                                      │          │
│     │   Chưa có tài khoản? Đăng ký ngay   │          │ <- Register Link
│     │                                      │          │
│     └──────────────────────────────────────┘          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Component Breakdown

**1. AuthLayout Component**
```typescript
interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle?: string;
  backgroundPattern?: 'north' | 'central' | 'south';
}

// Features:
// - Vietnamese-themed background gradient
// - Language toggle in header
// - VeriSyntra logo with link to landing page
// - Responsive design (mobile/tablet/desktop)
```

**2. LoginForm Component**
```typescript
interface LoginFormProps {
  onSubmit: (credentials: LoginCredentials) => Promise<void>;
  isLoading: boolean;
  error: string | null;
}

// Features:
// - Email validation (Vietnamese business email format)
// - Password visibility toggle
// - Form validation with Vietnamese error messages
// - Loading state with spinner
// - Remember me checkbox
// - Accessible (ARIA labels, keyboard navigation)
```

**3. Input Field Variants**
```typescript
// EmailInput.tsx
<div className="veri-input-group">
  <label htmlFor="email" className="veri-label">
    {isVietnamese ? 'Email' : 'Email Address'}
  </label>
  <input
    id="email"
    type="email"
    className="veri-input"
    placeholder={isVietnamese ? 'ten@congty.vn' : 'name@company.vn'}
    {...register('email', {
      required: isVietnamese 
        ? 'Vui lòng nhập email' 
        : 'Email is required',
      pattern: {
        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
        message: isVietnamese 
          ? 'Email không hợp lệ' 
          : 'Invalid email address'
      }
    })}
  />
  {errors.email && (
    <span className="veri-error">{errors.email.message}</span>
  )}
</div>

// PasswordInput.tsx (with visibility toggle)
<div className="veri-input-group">
  <label htmlFor="password" className="veri-label">
    {isVietnamese ? 'Mật khẩu' : 'Password'}
  </label>
  <div className="veri-password-wrapper">
    <input
      id="password"
      type={showPassword ? 'text' : 'password'}
      className="veri-input"
      placeholder={isVietnamese ? '••••••••' : '••••••••'}
      {...register('password', {
        required: isVietnamese 
          ? 'Vui lòng nhập mật khẩu' 
          : 'Password is required',
        minLength: {
          value: 8,
          message: isVietnamese 
            ? 'Mật khẩu phải có ít nhất 8 ký tự' 
            : 'Password must be at least 8 characters'
        }
      })}
    />
    <button
      type="button"
      onClick={() => setShowPassword(!showPassword)}
      className="veri-password-toggle"
    >
      {showPassword ? <EyeOff /> : <Eye />}
    </button>
  </div>
  {errors.password && (
    <span className="veri-error">{errors.password.message}</span>
  )}
</div>
```

---

## 5. Form Validation Rules

### Client-Side Validation
```typescript
import { useForm } from 'react-hook-form';

interface LoginFormData {
  email: string;
  password: string;
  rememberMe: boolean;
  tenantId?: string; // Optional: auto-filled from query params or stored
}

const validationRules = {
  email: {
    required: {
      vi: 'Vui lòng nhập địa chỉ email',
      en: 'Email address is required'
    },
    pattern: {
      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
      message: {
        vi: 'Địa chỉ email không hợp lệ',
        en: 'Invalid email address'
      }
    }
  },
  password: {
    required: {
      vi: 'Vui lòng nhập mật khẩu',
      en: 'Password is required'
    },
    minLength: {
      value: 8,
      message: {
        vi: 'Mật khẩu phải có ít nhất 8 ký tự',
        en: 'Password must be at least 8 characters'
      }
    }
  }
};
```

### Server-Side Error Handling
```typescript
// authService.ts
export const login = async (credentials: LoginCredentials): Promise<LoginResponse> => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/v1/auth/login`,
      credentials,
      {
        headers: { 'Content-Type': 'application/json' }
      }
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      // Handle specific error codes
      if (error.response?.status === 401) {
        throw new Error(
          error.response.data?.detail?.message || 
          'Invalid email or password'
        );
      } else if (error.response?.status === 403) {
        throw new Error(
          error.response.data?.detail?.message || 
          'Account is inactive'
        );
      } else if (error.response?.status === 422) {
        // Validation errors
        const details = error.response.data?.detail;
        if (Array.isArray(details)) {
          const messages = details.map(d => d.msg).join(', ');
          throw new Error(messages);
        }
      }
    }
    throw new Error('An unexpected error occurred. Please try again.');
  }
};
```

---

## 6. Tenant ID Management

### Challenge
The login endpoint requires a `tenant_id`, but users typically don't know their UUID.

### Solution Options

**Option 1: Email-Based Tenant Lookup (RECOMMENDED)**
```typescript
// Add new endpoint to auth service:
// GET /api/v1/auth/tenants/lookup?email={email}

// Response:
{
  "tenant_id": "uuid",
  "company_name": "VeriSyntra Vietnam",
  "company_name_vi": "VeriSyntra Việt Nam"
}

// Flow:
1. User enters email
2. On blur, call lookup endpoint
3. Auto-fill tenant_id (hidden field)
4. Submit login with tenant_id
```

**Option 2: Subdomain-Based Tenancy**
```typescript
// Example: acme.verisyntra.vn
// Extract tenant from subdomain

const getTenantFromSubdomain = (): string | null => {
  const host = window.location.hostname;
  const parts = host.split('.');
  if (parts.length >= 3) {
    return parts[0]; // e.g., 'acme'
  }
  return null;
};
```

**Option 3: Two-Step Login**
```typescript
// Step 1: Enter email
// Step 2: System shows company name, user enters password

// UI:
"Đăng nhập vào VeriSyntra Vietnam"
"Logging into VeriSyntra Vietnam"
```

**Implementation (Option 1 - Recommended):**
```typescript
const handleEmailBlur = async (email: string) => {
  if (!email || !isValidEmail(email)) return;
  
  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/v1/auth/tenants/lookup?email=${email}`
    );
    setTenantId(response.data.tenant_id);
    setCompanyName(response.data.company_name_vi);
  } catch (error) {
    // Email not found, will show error on submit
    console.log('Tenant lookup failed, continuing...');
  }
};
```

---

## 7. Translation Keys

### Vietnamese (`locales/vi/auth.json`)
```json
{
  "login": {
    "title": "Chào mừng trở lại",
    "subtitle": "Đăng nhập vào VeriSyntra",
    "emailLabel": "Địa chỉ email",
    "emailPlaceholder": "ten@congty.vn",
    "passwordLabel": "Mật khẩu",
    "passwordPlaceholder": "Nhập mật khẩu của bạn",
    "rememberMe": "Ghi nhớ đăng nhập",
    "forgotPassword": "Quên mật khẩu?",
    "submitButton": "Đăng nhập",
    "submitting": "Đang đăng nhập...",
    "noAccount": "Chưa có tài khoản?",
    "registerLink": "Đăng ký ngay",
    "errors": {
      "emailRequired": "Vui lòng nhập địa chỉ email",
      "emailInvalid": "Địa chỉ email không hợp lệ",
      "passwordRequired": "Vui lòng nhập mật khẩu",
      "passwordTooShort": "Mật khẩu phải có ít nhất 8 ký tự",
      "invalidCredentials": "Email hoặc mật khẩu không đúng",
      "accountInactive": "Tài khoản đã bị vô hiệu hóa. Vui lòng liên hệ quản trị viên.",
      "networkError": "Lỗi kết nối. Vui lòng thử lại."
    },
    "success": {
      "login": "Đăng nhập thành công! Đang chuyển hướng...",
      "welcome": "Chào mừng, {name}!"
    }
  }
}
```

### English (`locales/en/auth.json`)
```json
{
  "login": {
    "title": "Welcome Back",
    "subtitle": "Sign in to VeriSyntra",
    "emailLabel": "Email Address",
    "emailPlaceholder": "name@company.vn",
    "passwordLabel": "Password",
    "passwordPlaceholder": "Enter your password",
    "rememberMe": "Remember me",
    "forgotPassword": "Forgot password?",
    "submitButton": "Sign In",
    "submitting": "Signing in...",
    "noAccount": "Don't have an account?",
    "registerLink": "Register now",
    "errors": {
      "emailRequired": "Email address is required",
      "emailInvalid": "Invalid email address",
      "passwordRequired": "Password is required",
      "passwordTooShort": "Password must be at least 8 characters",
      "invalidCredentials": "Invalid email or password",
      "accountInactive": "Account is inactive. Please contact administrator.",
      "networkError": "Connection error. Please try again."
    },
    "success": {
      "login": "Login successful! Redirecting...",
      "welcome": "Welcome, {name}!"
    }
  }
}
```

---

## 8. Implementation Steps

### Phase 1: Setup (Day 1)
- [STEP] Create folder structure: `src/components/Auth/Login/`
- [STEP] Create translation files: `locales/vi/auth.json`, `locales/en/auth.json`
- [STEP] Set up Zustand auth store: `src/stores/authStore.ts`
- [STEP] Create token manager utility: `src/services/auth/tokenManager.ts`
- [STEP] Create auth service API client: `src/services/auth/authService.ts`

### Phase 2: Components (Day 2)
- [STEP] Build AuthLayout component (shared layout for login/register)
- [STEP] Build LoginForm component with react-hook-form
- [STEP] Create reusable input components (EmailInput, PasswordInput)
- [STEP] Add form validation with Vietnamese error messages

### Phase 3: Integration (Day 3)
- [STEP] Connect LoginForm to auth service API
- [STEP] Implement JWT token storage in localStorage
- [STEP] Add loading states and error handling
- [STEP] Implement "Remember Me" functionality
- [STEP] Add redirect after successful login

### Phase 4: Routing (Day 4)
- [STEP] Update AppRouter.tsx to add `/login` route
- [STEP] Create ProtectedRoute component for authenticated routes
- [STEP] Redirect unauthenticated users from `/app` to `/login`
- [STEP] Implement logout functionality

### Phase 5: Testing & Polish (Day 5)
- [STEP] Test with real auth service API (localhost:8001)
- [STEP] Test form validation edge cases
- [STEP] Test responsive design (mobile/tablet/desktop)
- [STEP] Add loading skeletons
- [STEP] Add success/error toast notifications
- [STEP] Test Vietnamese/English language switching

---

## 9. Code Templates

### LoginPage.tsx (Main Component)
```typescript
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useForm } from 'react-hook-form';
import { useAuthStore } from '../../stores/authStore';
import AuthLayout from '../shared/AuthLayout';
import { Eye, EyeOff, Mail, Lock } from 'lucide-react';

interface LoginFormData {
  email: string;
  password: string;
  rememberMe: boolean;
}

function LoginPage() {
  const { t } = useTranslation('auth');
  const navigate = useNavigate();
  const { login, isLoading, error } = useAuthStore();
  const [showPassword, setShowPassword] = useState(false);
  const [tenantId, setTenantId] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError
  } = useForm<LoginFormData>({
    defaultValues: {
      rememberMe: true
    }
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      // TODO: Implement tenant lookup if tenantId is null
      if (!tenantId) {
        setError('email', {
          message: t('login.errors.emailNotFound')
        });
        return;
      }

      await login({
        email: data.email,
        password: data.password,
        tenant_id: tenantId
      });

      // Success - redirect to dashboard
      navigate('/app');
    } catch (err) {
      // Error handling already in store
      console.error('Login failed:', err);
    }
  };

  return (
    <AuthLayout
      title={t('login.title')}
      subtitle={t('login.subtitle')}
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Email Input */}
        <div className="veri-input-group">
          <label htmlFor="email" className="veri-label">
            {t('login.emailLabel')}
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Mail className="h-5 w-5 text-gray-400" />
            </div>
            <input
              id="email"
              type="email"
              className={`veri-input pl-10 ${errors.email ? 'border-red-500' : ''}`}
              placeholder={t('login.emailPlaceholder')}
              {...register('email', {
                required: t('login.errors.emailRequired'),
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: t('login.errors.emailInvalid')
                }
              })}
            />
          </div>
          {errors.email && (
            <span className="veri-error">{errors.email.message}</span>
          )}
        </div>

        {/* Password Input */}
        <div className="veri-input-group">
          <label htmlFor="password" className="veri-label">
            {t('login.passwordLabel')}
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Lock className="h-5 w-5 text-gray-400" />
            </div>
            <input
              id="password"
              type={showPassword ? 'text' : 'password'}
              className={`veri-input pl-10 pr-10 ${errors.password ? 'border-red-500' : ''}`}
              placeholder={t('login.passwordPlaceholder')}
              {...register('password', {
                required: t('login.errors.passwordRequired'),
                minLength: {
                  value: 8,
                  message: t('login.errors.passwordTooShort')
                }
              })}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute inset-y-0 right-0 pr-3 flex items-center"
            >
              {showPassword ? (
                <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-600" />
              ) : (
                <Eye className="h-5 w-5 text-gray-400 hover:text-gray-600" />
              )}
            </button>
          </div>
          {errors.password && (
            <span className="veri-error">{errors.password.message}</span>
          )}
        </div>

        {/* Remember Me & Forgot Password */}
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              id="rememberMe"
              type="checkbox"
              className="veri-checkbox"
              {...register('rememberMe')}
            />
            <label htmlFor="rememberMe" className="ml-2 text-sm text-gray-700">
              {t('login.rememberMe')}
            </label>
          </div>
          <Link
            to="/forgot-password"
            className="text-sm font-medium hover:underline"
            style={{ color: 'var(--veri-blue)' }}
          >
            {t('login.forgotPassword')}
          </Link>
        </div>

        {/* Error Message */}
        {error && (
          <div className="veri-error-banner">
            {error}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="veri-button-primary w-full"
        >
          {isLoading ? t('login.submitting') : t('login.submitButton')}
        </button>

        {/* Register Link */}
        <p className="text-center text-sm text-gray-600">
          {t('login.noAccount')}{' '}
          <Link
            to="/register"
            className="font-medium hover:underline"
            style={{ color: 'var(--veri-green)' }}
          >
            {t('login.registerLink')}
          </Link>
        </p>
      </form>
    </AuthLayout>
  );
}

export default LoginPage;
```

### authStore.ts (Zustand State Management)
```typescript
import { create } from 'zustand';
import { authService } from '../services/auth/authService';
import { tokenManager } from '../services/auth/tokenManager';

interface VeriUser {
  user_id: string;
  email: string;
  full_name: string;
  tenant_id: string;
  role: string;
}

interface VeriBusinessContext {
  veriBusinessId: string;
  veriRegionalLocation: string;
  veriIndustryType: string;
  veriSubscriptionTier: string;
}

interface LoginCredentials {
  email: string;
  password: string;
  tenant_id: string;
}

interface AuthState {
  user: VeriUser | null;
  veriBusinessContext: VeriBusinessContext | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  refreshAccessToken: () => Promise<void>;
  initializeAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  veriBusinessContext: null,
  accessToken: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  login: async (credentials) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authService.login(credentials);
      
      // Store tokens
      tokenManager.saveTokens(response.access_token, response.refresh_token);
      tokenManager.saveUser(response.user);
      tokenManager.saveBusinessContext(response.veri_business_context);

      set({
        user: response.user,
        veriBusinessContext: response.veri_business_context,
        accessToken: response.access_token,
        refreshToken: response.refresh_token,
        isAuthenticated: true,
        isLoading: false,
        error: null
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Login failed';
      set({
        isLoading: false,
        error: message,
        isAuthenticated: false
      });
      throw error;
    }
  },

  logout: () => {
    tokenManager.clearTokens();
    set({
      user: null,
      veriBusinessContext: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      error: null
    });
  },

  refreshAccessToken: async () => {
    const refreshToken = tokenManager.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    try {
      const response = await authService.refreshToken(refreshToken);
      tokenManager.saveTokens(response.access_token, response.refresh_token);
      
      set({
        accessToken: response.access_token,
        refreshToken: response.refresh_token
      });
    } catch (error) {
      // Refresh failed, logout user
      useAuthStore.getState().logout();
      throw error;
    }
  },

  initializeAuth: () => {
    const user = tokenManager.getUser();
    const accessToken = tokenManager.getAccessToken();
    const refreshToken = tokenManager.getRefreshToken();
    const businessContext = tokenManager.getBusinessContext();

    if (user && accessToken) {
      set({
        user,
        veriBusinessContext: businessContext,
        accessToken,
        refreshToken,
        isAuthenticated: true
      });
    }
  }
}));
```

---

## 10. Security Considerations

### CORS Configuration
Ensure auth service allows requests from frontend:
```yaml
# docker-compose.yml (already configured)
environment:
  - FRONTEND_URL=http://localhost:5173
```

### Token Security
```typescript
// Use httpOnly cookies for production (more secure)
// For development, localStorage is acceptable

// Add token expiration check
const isTokenExpired = (token: string): boolean => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.exp * 1000 < Date.now();
  } catch {
    return true;
  }
};
```

### HTTPS in Production
```typescript
// Enforce HTTPS in production
if (import.meta.env.PROD && window.location.protocol !== 'https:') {
  window.location.href = window.location.href.replace('http:', 'https:');
}
```

---

## 11. Accessibility Requirements

- [STEP] All form inputs have associated labels
- [STEP] Error messages announced to screen readers
- [STEP] Keyboard navigation support (Tab, Enter)
- [STEP] Focus management (auto-focus email on load)
- [STEP] ARIA labels for icon buttons
- [STEP] Color contrast meets WCAG AA standards

---

## 12. Testing Checklist

### Functional Testing
- [TEST] Login with valid credentials -> Success
- [TEST] Login with invalid email -> Error message
- [TEST] Login with wrong password -> Error message
- [TEST] Login with inactive account -> Inactive error
- [TEST] Remember me saves credentials
- [TEST] Language toggle switches UI
- [TEST] Redirect to dashboard after login
- [TEST] Token stored in localStorage
- [TEST] Logout clears tokens

### Edge Cases
- [TEST] Empty email field
- [TEST] Empty password field
- [TEST] Invalid email format
- [TEST] Password too short
- [TEST] Network error handling
- [TEST] API timeout handling

### Responsive Design
- [TEST] Mobile (320px - 767px)
- [TEST] Tablet (768px - 1023px)
- [TEST] Desktop (1024px+)

---

## 13. Next Steps After Login Page

1. **Registration Page** (see Registration_Page_Implementation_Plan.md)
2. **Protected Routes** - Redirect unauthenticated users
3. **Forgot Password Flow** - Password reset functionality
4. **Email Verification** - Verify email after registration
5. **Two-Factor Authentication (2FA)** - Optional security layer

---

## 14. Estimated Timeline

**Total Time:** 3-5 days (1 developer)

| Phase | Time | Status |
|-------|------|--------|
| Setup & Architecture | 4 hours | [PENDING] |
| Component Development | 8 hours | [PENDING] |
| API Integration | 4 hours | [PENDING] |
| Routing & Navigation | 2 hours | [PENDING] |
| Testing & Polish | 4 hours | [PENDING] |
| **Total** | **22 hours** | **[PENDING]** |

---

## 15. References

- **Auth Service API Docs:** http://localhost:8001/docs
- **VeriSyntra Color Palette:** `.github/copilot-instructions.md`
- **React Hook Form:** https://react-hook-form.com/
- **Zustand:** https://github.com/pmndrs/zustand
- **i18next:** https://react.i18next.com/

---

**Status:** Ready for implementation  
**Priority:** HIGH (blocking user authentication)  
**Dependencies:** Phase 2 auth service (COMPLETED ✅)
