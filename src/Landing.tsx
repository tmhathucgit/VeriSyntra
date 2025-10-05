import { Shield, CheckCircle, Lock, FileText, Users, ArrowRight, Menu, X } from 'lucide-react';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useLanguageSwitch } from './hooks/useCulturalIntelligence';
import vnMapLogo from '../svg/vnMapLogo.svg';

function Landing() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { t } = useTranslation(['common', 'veriportal']);
  const { switchLanguage, isVietnamese } = useLanguageSwitch();

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed w-full bg-white/95 backdrop-blur-sm z-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <Link to="/app" className="flex items-center group">
              <div className="flex items-center space-x-0 group-hover:scale-105 transition-transform">
                <img src={vnMapLogo} alt="VeriSyntra Logo" className="w-8 h-8" />
                <span className="text-xl font-bold text-slate-800">VeriSyntra</span>
              </div>
            </Link>

            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">{t('veriportal:navigation.features')}</a>
              <a href="#benefits" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">{t('veriportal:navigation.benefits')}</a>
              <a href="#about" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">{t('veriportal:navigation.about')}</a>
              <a href="#contact" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">{t('veriportal:navigation.contact')}</a>
              <button 
                onClick={() => switchLanguage(isVietnamese ? 'en' : 'vi')}
                className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium border border-gray-300 px-3 py-1.5 rounded-md"
              >
                {isVietnamese ? 'EN' : 'VI'}
              </button>
              <Link to="/app" className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-2.5 rounded-lg font-medium transition-all transform hover:scale-105 shadow-sm inline-block">
                {t('veriportal:hero.getStarted')}
              </Link>
            </div>

            <button
              className="md:hidden text-gray-600"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {mobileMenuOpen && (
          <div className="md:hidden border-t border-gray-100 bg-white">
            <div className="px-4 py-4 space-y-3">
              <a href="#features" className="block text-gray-600 hover:text-gray-900 py-2">Tính năng</a>
              <a href="#benefits" className="block text-gray-600 hover:text-gray-900 py-2">Lợi ích</a>
              <a href="#about" className="block text-gray-600 hover:text-gray-900 py-2">Về chúng tôi</a>
              <a href="#contact" className="block text-gray-600 hover:text-gray-900 py-2">Liên hệ</a>
              <Link to="/app" className="block w-full bg-teal-600 hover:bg-teal-700 text-white px-6 py-2.5 rounded-lg font-medium text-center">
                {t('veriportal:hero.getStarted')}
              </Link>
            </div>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-orange-50 via-teal-50 to-emerald-50">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="inline-flex items-center space-x-2 bg-emerald-100 text-emerald-700 px-4 py-2 rounded-full text-sm font-medium">
                <Shield size={16} />
                <span>{t('veriportal:hero.badge')}</span>
              </div>

              <h1 className="text-5xl sm:text-6xl font-bold text-gray-900 leading-tight">
                {t('veriportal:hero.title').split('PDPL 2025')[0]}{' '}
                <span className="text-orange-500 bg-gradient-to-r from-orange-500 to-emerald-600 bg-clip-text text-transparent">
                  PDPL 2025
                </span>{' '}
                {t('veriportal:hero.title').split('PDPL 2025')[1]}
              </h1>

              <p className="text-xl text-gray-600 leading-relaxed">
                {t('veriportal:hero.subtitle')}
              </p>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/veriportal" className="group bg-gradient-to-r from-red-600 via-yellow-500 to-red-600 hover:from-red-700 hover:via-yellow-600 hover:to-red-700 text-white px-8 py-4 rounded-xl font-semibold transition-all transform hover:scale-105 shadow-lg hover:shadow-xl flex items-center justify-center space-x-2">
                  <span className="flex items-center gap-2">
                    🇻🇳 {isVietnamese ? 'VeriPortal - Onboarding Văn hóa Việt' : 'VeriPortal - Vietnamese Cultural Onboarding'}
                  </span>
                  <ArrowRight className="group-hover:translate-x-1 transition-transform" size={20} />
                </Link>
                <Link to="/app" className="group bg-teal-600 hover:bg-teal-700 text-white px-8 py-4 rounded-xl font-semibold transition-all transform hover:scale-105 shadow-lg hover:shadow-xl flex items-center justify-center space-x-2">
                  <span>{t('veriportal:hero.tryFree')}</span>
                  <ArrowRight className="group-hover:translate-x-1 transition-transform" size={20} />
                </Link>
                <Link to="/app" className="bg-white hover:bg-gray-50 text-teal-600 px-8 py-4 rounded-xl font-semibold border-2 border-teal-600 transition-all flex items-center justify-center">
                  {t('veriportal:hero.enterApp')}
                </Link>
              </div>

              <div className="flex items-center space-x-8 pt-4">
                <div>
                  <div className="text-3xl font-bold text-gray-900">500+</div>
                  <div className="text-sm text-gray-600">{t('veriportal:stats.trustedBusinesses')}</div>
                </div>
                <div className="h-12 w-px bg-gray-300"></div>
                <div>
                  <div className="text-3xl font-bold text-gray-900">99.9%</div>
                  <div className="text-sm text-gray-600">{t('veriportal:stats.complianceRate')}</div>
                </div>
                <div className="h-12 w-px bg-gray-300"></div>
                <div>
                  <div className="text-3xl font-bold text-gray-900">24/7</div>
                  <div className="text-sm text-gray-600">{t('veriportal:stats.support')}</div>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-tr from-orange-200 to-emerald-300 rounded-3xl transform rotate-3 opacity-20"></div>
              <div className="relative bg-white rounded-3xl shadow-2xl p-8 border border-gray-100">
                <div className="space-y-6">
                  <div className="flex items-start space-x-4 p-4 bg-green-50 rounded-xl border border-green-100">
                    <CheckCircle className="text-green-500 flex-shrink-0 mt-1" size={24} />
                    <div>
                      <h3 className="font-semibold text-gray-900">Đánh giá tự động</h3>
                      <p className="text-sm text-gray-600 mt-1">Hệ thống tự động đánh giá mức độ tuân thủ PDPL</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4 p-4 bg-emerald-50 rounded-xl border border-emerald-100">
                    <Lock className="text-emerald-600 flex-shrink-0 mt-1" size={24} />
                    <div>
                      <h3 className="font-semibold text-gray-900">Bảo mật dữ liệu</h3>
                      <p className="text-sm text-gray-600 mt-1">Quản lý và bảo vệ dữ liệu cá nhân theo chuẩn quốc tế</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4 p-4 bg-orange-50 rounded-xl border border-orange-100">
                    <FileText className="text-orange-500 flex-shrink-0 mt-1" size={24} />
                    <div>
                      <h3 className="font-semibold text-gray-900">Tài liệu hoàn chỉnh</h3>
                      <p className="text-sm text-gray-600 mt-1">Tạo tự động các tài liệu tuân thủ cần thiết</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4 p-4 bg-cyan-50 rounded-xl border border-cyan-100">
                    <Users className="text-cyan-600 flex-shrink-0 mt-1" size={24} />
                    <div>
                      <h3 className="font-semibold text-gray-900">Đào tạo nhân viên</h3>
                      <p className="text-sm text-gray-600 mt-1">Khóa học và tài liệu đào tạo cho đội ngũ</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Tính năng nổi bật
            </h2>
            <p className="text-xl text-gray-600">
              Giải pháp toàn diện giúp doanh nghiệp tuân thủ PDPL 2025 một cách dễ dàng
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Shield,
                title: 'Đánh giá tuân thủ',
                description: 'Đánh giá tự động và chi tiết mức độ tuân thủ PDPL của doanh nghiệp',
                color: 'bg-orange-100 text-orange-500'
              },
              {
                icon: FileText,
                title: 'Quản lý tài liệu',
                description: 'Tạo và quản lý tất cả tài liệu cần thiết cho việc tuân thủ',
                color: 'bg-emerald-100 text-emerald-600'
              },
              {
                icon: Lock,
                title: 'Bảo mật dữ liệu',
                description: 'Công cụ quản lý và bảo vệ dữ liệu cá nhân theo tiêu chuẩn cao',
                color: 'bg-teal-100 text-teal-600'
              },
              {
                icon: Users,
                title: 'Đào tạo & Hướng dẫn',
                description: 'Khóa học và tài liệu đào tạo cho nhân viên về PDPL',
                color: 'bg-cyan-100 text-cyan-600'
              },
              {
                icon: CheckCircle,
                title: 'Theo dõi tiến độ',
                description: 'Dashboard theo dõi tiến độ tuân thủ theo thời gian thực',
                color: 'bg-lime-100 text-lime-600'
              },
              {
                icon: Shield,
                title: 'Cập nhật liên tục',
                description: 'Cập nhật tự động khi có thay đổi về quy định PDPL',
                color: 'bg-green-100 text-green-600'
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="group p-8 bg-white rounded-2xl border border-gray-100 hover:border-orange-200 hover:shadow-xl transition-all duration-300"
              >
                <div className={`w-14 h-14 ${feature.color} rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                  <feature.icon size={28} />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-orange-50 to-emerald-50">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Tại sao chọn VeriSyntra?
              </h2>
              <div className="space-y-6">
                {[
                  {
                    title: 'Tiết kiệm chi phí',
                    description: 'Giảm đến 70% chi phí so với việc thuê tư vấn bên ngoài'
                  },
                  {
                    title: 'Tiết kiệm thời gian',
                    description: 'Đạt tuân thủ trong vòng 4-6 tuần thay vì 6-12 tháng'
                  },
                  {
                    title: 'Dễ sử dụng',
                    description: 'Giao diện thân thiện, không cần kiến thức chuyên môn sâu'
                  },
                  {
                    title: 'Hỗ trợ tiếng Việt',
                    description: 'Hoàn toàn bằng tiếng Việt, phù hợp với doanh nghiệp Việt Nam'
                  }
                ].map((benefit, index) => (
                  <div key={index} className="flex items-start space-x-4">
                    <div className="flex-shrink-0 w-6 h-6 bg-emerald-600 rounded-full flex items-center justify-center mt-1">
                      <CheckCircle size={16} className="text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 text-lg mb-1">{benefit.title}</h3>
                      <p className="text-gray-600">{benefit.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-3xl shadow-2xl p-8 border border-gray-100">
              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{t('veriportal:cta.startToday')}</h3>
                <p className="text-gray-600">Dùng thử miễn phí 14 ngày, không cần thẻ tín dụng</p>
              </div>

              <form className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tên doanh nghiệp
                  </label>
                  <input
                    type="text"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                    placeholder="Công ty ABC"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email công ty
                  </label>
                  <input
                    type="email"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                    placeholder="contact@company.com"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Số điện thoại
                  </label>
                  <input
                    type="tel"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                    placeholder="0901234567"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full bg-teal-600 hover:bg-teal-700 text-white px-8 py-4 rounded-xl font-semibold transition-all transform hover:scale-105 shadow-lg hover:shadow-xl"
                >
                  Đăng ký dùng thử miễn phí
                </button>
              </form>

              <p className="text-center text-sm text-gray-500 mt-6">
                Bằng cách đăng ký, bạn đồng ý với{' '}
                <a href="#" className="text-orange-500 hover:underline">Điều khoản dịch vụ</a>
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-teal-600 to-emerald-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
            {t('veriportal:cta.title')}
          </h2>
          <p className="text-xl text-teal-100 mb-8 leading-relaxed">
            {t('veriportal:cta.subtitle')}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/app" 
              className="group bg-white hover:bg-gray-100 text-teal-600 px-8 py-4 rounded-xl font-semibold transition-all transform hover:scale-105 shadow-lg hover:shadow-xl flex items-center justify-center space-x-2"
            >
              <Shield className="w-5 h-5" />
              <span>{t('veriportal:cta.enterVeriSyntra')}</span>
              <ArrowRight className="group-hover:translate-x-1 transition-transform w-5 h-5" />
            </Link>
            <Link 
              to="/app" 
              className="bg-teal-700 hover:bg-teal-800 text-white px-8 py-4 rounded-xl font-semibold border-2 border-teal-400 transition-all flex items-center justify-center space-x-2"
            >
              <span>{t('veriportal:hero.liveDemo')}</span>
            </Link>
          </div>
          <div className="mt-8 text-teal-100 text-sm">
            ✅ Miễn phí dùng thử • ✅ Hỗ trợ tiếng Việt • ✅ Tuân thủ văn hóa doanh nghiệp Việt Nam
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center space-x-0 mb-4">
                <img src={vnMapLogo} alt="VeriSyntra Logo" className="w-8 h-8" />
                <span className="text-xl font-bold text-white">VeriSyntra</span>
              </div>
              <p className="text-sm text-gray-400 leading-relaxed">
                Giải pháp tuân thủ PDPL 2025 hàng đầu cho doanh nghiệp Việt Nam
              </p>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">Sản phẩm</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">Tính năng</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Bảng giá</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Tài liệu</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">Công ty</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">Về chúng tôi</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Liên hệ</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">Hỗ trợ</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">Trung tâm hỗ trợ</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Điều khoản dịch vụ</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Chính sách bảo mật</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-gray-400">
              © 2025 VeriSyntra. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">Facebook</a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">LinkedIn</a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">Twitter</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Landing;
