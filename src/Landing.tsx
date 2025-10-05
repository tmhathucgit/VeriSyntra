import { Shield, CheckCircle, Lock, FileText, Users, ArrowRight, Menu, X, Globe } from 'lucide-react';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useLanguageSwitch } from './hooks/useCulturalIntelligence';
import vnMapLogo from '../svg/vnMapLogo.svg';

function Landing() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { t } = useTranslation(['common', 'landing']);
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
              <a href="#features" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">{t('landing:navigation.features')}</a>
              <a href="#benefits" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">{t('landing:navigation.benefits')}</a>
              <a href="#about" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">{t('landing:navigation.about')}</a>
              <a href="#contact" className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium">{t('landing:navigation.contact')}</a>
              <Link to="/veriportal" className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-2.5 rounded-lg font-medium transition-all transform hover:scale-105 shadow-sm inline-block">
                {t('veriportal:hero.getStarted')}
              </Link>
              <button 
                onClick={() => switchLanguage(isVietnamese ? 'en' : 'vi')}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors"
              >
                <Globe className="w-4 h-4" />
                <span className="font-medium">{t('common:language.current')}</span>
              </button>
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
              <a href="#features" className="block text-gray-600 hover:text-gray-900 py-2">{t('landing:navigation.features')}</a>
              <a href="#benefits" className="block text-gray-600 hover:text-gray-900 py-2">{t('landing:navigation.benefits')}</a>
              <a href="#about" className="block text-gray-600 hover:text-gray-900 py-2">{t('landing:navigation.about')}</a>
              <a href="#contact" className="block text-gray-600 hover:text-gray-900 py-2">{t('landing:navigation.contact')}</a>
              <Link to="/veriportal" className="block w-full bg-teal-600 hover:bg-teal-700 text-white px-6 py-2.5 rounded-lg font-medium text-center mb-2">
                {t('landing:hero.getStarted')}
              </Link>
              <button 
                onClick={() => switchLanguage(isVietnamese ? 'en' : 'vi')}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors w-full justify-center"
              >
                <Globe className="w-4 h-4" />
                <span className="font-medium">{t('common:language.current')}</span>
              </button>
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
                <span>{t('landing:hero.badge')}</span>
              </div>

              <h1 className="text-5xl sm:text-6xl font-bold text-gray-900 leading-tight">
                {t('landing:hero.title').split('PDPL 2025')[0]}{' '}
                <span className="text-orange-500 bg-gradient-to-r from-orange-500 to-emerald-600 bg-clip-text text-transparent">
                  PDPL 2025
                </span>{' '}
                {t('landing:hero.title').split('PDPL 2025')[1]}
              </h1>

              <p className="text-xl text-gray-600 leading-relaxed">
                {t('landing:hero.subtitle')}
              </p>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/app" className="bg-white hover:bg-gray-50 text-teal-600 px-8 py-4 rounded-xl font-semibold border-2 border-teal-600 transition-all flex items-center justify-center">
                  {t('landing:hero.enterApp')}
                </Link>
              </div>

              <div className="flex items-center space-x-8 pt-4">
                <div>
                  <div className="text-3xl font-bold text-gray-900">500+</div>
                  <div className="text-sm text-gray-600">{t('landing:stats.trustedBusinesses')}</div>
                </div>
                <div className="h-12 w-px bg-gray-300"></div>
                <div>
                  <div className="text-3xl font-bold text-gray-900">99.9%</div>
                  <div className="text-sm text-gray-600">{t('landing:stats.complianceRate')}</div>
                </div>
                <div className="h-12 w-px bg-gray-300"></div>
                <div>
                  <div className="text-3xl font-bold text-gray-900">24/7</div>
                  <div className="text-sm text-gray-600">{t('landing:stats.support')}</div>
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
                      <h3 className="font-semibold text-gray-900">{t('landing:features.automaticAssessment.title')}</h3>
                      <p className="text-sm text-gray-600 mt-1">{t('landing:features.automaticAssessment.description')}</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4 p-4 bg-emerald-50 rounded-xl border border-emerald-100">
                    <Lock className="text-emerald-600 flex-shrink-0 mt-1" size={24} />
                    <div>
                      <h3 className="font-semibold text-gray-900">{t('landing:features.dataProtection.title')}</h3>
                      <p className="text-sm text-gray-600 mt-1">{t('landing:features.dataProtection.description')}</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4 p-4 bg-orange-50 rounded-xl border border-orange-100">
                    <FileText className="text-orange-500 flex-shrink-0 mt-1" size={24} />
                    <div>
                      <h3 className="font-semibold text-gray-900">{t('landing:features.documentGeneration.title')}</h3>
                      <p className="text-sm text-gray-600 mt-1">{t('landing:features.documentGeneration.description')}</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4 p-4 bg-cyan-50 rounded-xl border border-cyan-100">
                    <Users className="text-cyan-600 flex-shrink-0 mt-1" size={24} />
                    <div>
                      <h3 className="font-semibold text-gray-900">{t('landing:features.staffTraining.title')}</h3>
                      <p className="text-sm text-gray-600 mt-1">{t('landing:features.staffTraining.description')}</p>
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
              {t('landing:features.title')}
            </h2>
            <p className="text-xl text-gray-600">
              {t('landing:features.description')}
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Shield,
                title: t('landing:features.complianceAssessment.title'),
                description: t('landing:features.complianceAssessment.description'),
                color: 'bg-orange-100 text-orange-500'
              },
              {
                icon: FileText,
                title: t('landing:features.documentManagement.title'),
                description: t('landing:features.documentManagement.description'),
                color: 'bg-emerald-100 text-emerald-600'
              },
              {
                icon: Lock,
                title: t('landing:features.dataProtection.title'),
                description: t('landing:features.dataProtection.description'),
                color: 'bg-teal-100 text-teal-600'
              },
              {
                icon: Users,
                title: t('landing:features.training.title'),
                description: t('landing:features.training.description'),
                color: 'bg-cyan-100 text-cyan-600'
              },
              {
                icon: CheckCircle,
                title: t('landing:features.progressTracking.title'),
                description: t('landing:features.progressTracking.description'),
                color: 'bg-lime-100 text-lime-600'
              },
              {
                icon: Shield,
                title: t('landing:features.continuousUpdates.title'),
                description: t('landing:features.continuousUpdates.description'),
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
                {t('landing:benefits.title')}
              </h2>
              <div className="space-y-6">
                {[
                  {
                    title: t('landing:benefits.costSaving.title'),
                    description: t('landing:benefits.costSaving.description')
                  },
                  {
                    title: t('landing:benefits.timeSaving.title'),
                    description: t('landing:benefits.timeSaving.description')
                  },
                  {
                    title: t('landing:benefits.easeOfUse.title'),
                    description: t('landing:benefits.easeOfUse.description')
                  },
                  {
                    title: t('landing:benefits.vietnameseSupport.title'),
                    description: t('landing:benefits.vietnameseSupport.description')
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
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{t('landing:cta.startToday')}</h3>
                <p className="text-gray-600">{t('landing:trial.description')}</p>
              </div>

              <form className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t('landing:form.businessName')}
                  </label>
                  <input
                    type="text"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                    placeholder={t('landing:form.businessNamePlaceholder')}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t('landing:form.companyEmail')}
                  </label>
                  <input
                    type="email"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                    placeholder={t('landing:form.emailPlaceholder')}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t('landing:form.phoneNumber')}
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
                  {t('landing:trial.signupButton')}
                </button>
              </form>

              <p className="text-center text-sm text-gray-500 mt-6">
                {t('landing:trial.agreement')}{' '}
                <a href="#" className="text-orange-500 hover:underline">{t('landing:footer.termsOfService')}</a>
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-teal-600 to-emerald-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
            {t('landing:cta.title')}
          </h2>
          <p className="text-xl text-teal-100 mb-8 leading-relaxed">
            {t('landing:cta.subtitle')}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/app" 
              className="group bg-white hover:bg-gray-100 text-teal-600 px-8 py-4 rounded-xl font-semibold transition-all transform hover:scale-105 shadow-lg hover:shadow-xl flex items-center justify-center space-x-2"
            >
              <Shield className="w-5 h-5" />
              <span>{t('landing:cta.enterVeriSyntra')}</span>
              <ArrowRight className="group-hover:translate-x-1 transition-transform w-5 h-5" />
            </Link>
            <Link 
              to="/app" 
              className="bg-teal-700 hover:bg-teal-800 text-white px-8 py-4 rounded-xl font-semibold border-2 border-teal-400 transition-all flex items-center justify-center space-x-2"
            >
              <span>{t('landing:hero.liveDemo')}</span>
            </Link>
          </div>
          <div className="mt-8 text-teal-100 text-sm">
            {t('landing:trial.benefits')}
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
                {t('landing:footer.companyDescription')}
              </p>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">{t('landing:footer.products')}</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">{t('landing:footer.features')}</a></li>
                <li><a href="#" className="hover:text-white transition-colors">{t('landing:footer.pricing')}</a></li>
                <li><a href="#" className="hover:text-white transition-colors">{t('landing:footer.documentation')}</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">{t('landing:footer.company')}</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">{t('landing:footer.aboutUs')}</a></li>
                <li><a href="#" className="hover:text-white transition-colors">{t('landing:footer.blog')}</a></li>
                <li><a href="#" className="hover:text-white transition-colors">{t('landing:footer.contact')}</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">{t('landing:footer.support')}</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">{t('landing:footer.helpCenter')}</a></li>
                <li><a href="#" className="hover:text-white transition-colors">{t('landing:footer.termsOfService')}</a></li>
                <li><a href="#" className="hover:text-white transition-colors">{t('landing:footer.privacyPolicy')}</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-gray-400">
              {t('landing:footer.copyright')}
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
