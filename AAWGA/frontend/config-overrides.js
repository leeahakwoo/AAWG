// config-overrides.js

const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

module.exports = function override(config, env) {
  if (env === 'production') {
    config.plugins.push(
      new BundleAnalyzerPlugin({
        analyzerMode: 'static',
        reportFilename: '../bundle-report.html',
        openAnalyzer: true,
      })
    );
  }
  return config;
};
