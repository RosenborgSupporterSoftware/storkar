/*!
 * backbone.layoutmanager.js v0.9.7
 * Copyright 2015, Tim Branyen (@tbranyen)
 * backbone.layoutmanager.js may be freely distributed under the MIT license.
 */
(function(c,a){if(typeof define==="function"&&define.amd){define(["backbone","underscore","jquery"],function(){return a.apply(c,arguments)})}else{if(typeof exports==="object"){var d=require("backbone");var b=require("underscore");d.$=d.$||require("jquery");module.exports=a.call(c,d,b,d.$)}else{a.call(c,c.Backbone,c._,c.Backbone.$)}}}(typeof global==="object"?global:this,function(k,l,f){var h=this;var b=k.View;var g=Array.prototype.push;var i=Array.prototype.concat;var c=Array.prototype.splice;var d=String.prototype.trim?l.bind(String.prototype.trim.call,String.prototype.trim):f.trim;var a=k.View.extend({_render:function(){var m=this;var p=m.__manager__;var o=m.beforeRender;var q=m.deferred();if(m.hasRendered){m._removeViews()}p.callback=function(){delete p.isAsync;delete p.callback;m.trigger("beforeRender",m);m._viewRender(p).render().then(function(){q.resolve()})};if(o){var n=o.call(m,m);if(n&&n.then){p.isAsync=true;n.then(function(){p.callback();q.resolve()},q.resolve)}if(n===false){return q.resolve()}}if(!p.isAsync){p.callback()}return q.promise()},_applyTemplate:function(o,m,n){if(l.isString(o)){if(m.noel){o=f.parseHTML(o,true);this.$el.slice(1).remove();this.$el.replaceWith(o);this.setElement(o,false)}else{this.html(this.$el,o)}}n.resolveWith(this,[this])},_viewRender:function(p){var o,q,r;var n=this;function m(s,t){var u;p.callback=function(v){delete p.isAsync;delete p.callback;n._applyTemplate(v,p,r)};a.cache(o,t);if(t){u=n.renderTemplate.call(n,t,s)}if(!p.isAsync){n._applyTemplate(u,p,r)}}return{render:function(){var s=n.serialize;var t=n.template;r=n.deferred();if(l.isFunction(s)){s=s.call(n)}p.callback=function(u){delete p.isAsync;delete p.callback;m(s,u)};if(typeof t==="string"){o=n.prefix+t}if(q=a.cache(o)){m(s,q,o);return r}if(typeof t==="string"){q=n.fetchTemplate.call(n,n.prefix+t)}else{if(typeof t==="function"){q=t}else{if(t!=null){q=n.fetchTemplate.call(n,t)}}}if(!p.isAsync){m(s,q)}return r}}},constructor:function j(m){this.manage=true;l.extend(this,m);k.View.apply(this,arguments)},async:function(){var m=this.__manager__;m.isAsync=true;return m.callback},promise:function(){return this.__manager__.renderDeferred.promise()},then:function(){return this.promise().then.apply(this,arguments)},renderViews:function(n){var m=this;var p=m.__manager__;var q=m.deferred();if(n&&l.isArray(n)){n=l.chain(n)}else{n=m.getViews(n)}var o=n.map(function(r){return r.render().__manager__.renderDeferred}).value();p.renderDeferred=q.promise();m.when(o).then(function(){q.resolveWith(m,[m])});return m},insertView:function(m,n){if(n){return this.setView(m,n,true)}return this.setView(m,true)},insertViews:function(m){if(l.isArray(m)){return this.setViews({"":m})}l.each(m,function(o,n){m[n]=l.isArray(o)?o:[o]});return this.setViews(m)},getView:function(m){if(m==null){m=arguments[1]}return this.getViews(m).first().value()},getViews:function(n){var m;if(typeof n==="string"){n=this.sections[n]||n;m=this.views[n]||[];return l.chain([].concat(m))}m=l.chain(this.views).map(function(o){return l.isArray(o)?o:[o]},this).flatten();if(typeof n==="object"){return m.where(n)}return typeof n==="function"?m.filter(n):m},removeView:function(n){var m;m=this.getViews(n).each(function(o){o.remove()});m.value();return m},setView:function(p,o,r){var q,m;var n=this;if(typeof p!=="string"){r=o;o=p;p=""}q=o.__manager__;if(!q){throw new Error("The argument associated with selector '"+p+"' is defined and a View.  Set `manage` property to true for Backbone.View instances.")}q.parent=n;m=q.selector=n.sections[p]||p;if(!r){if(n.getView(p)!==o){n.removeView(p)}return n.views[m]=o}n.views[m]=i.call([],n.views[p]||[],o);n.__manager__.insert=true;return o},setViews:function(m){l.each(m,function(n,o){if(l.isArray(n)){return l.each(n,function(p){this.insertView(o,p)},this)}this.setView(o,n)},this);return this},render:function(){var m=this;var p=m.__manager__;var q=p.parent;var o=q&&q.__manager__;var s=m.deferred();function r(){l.each(m.views,function(v,u){if(l.isArray(v)){m.htmlBatch(m,v,u)}});if(q&&!p.insertedViaFragment){if(!m.contains(q.el,m.el)){q.partial(q.$el,m.$el,o,p)}}m.delegateEvents();m.hasRendered=true;p.renderInProgress=false;delete p.triggeredByRAF;if(p.queue&&p.queue.length){(p.queue.shift())()}else{delete p.queue}function t(){var u=h.console;var v=m.afterRender;if(v){v.call(m,m)}m.trigger("afterRender",m);if(p.noel&&m.$el.length>1){if(l.isFunction(u.warn)&&!m.suppressWarnings){u.warn("`el: false` with multiple top level elements is not supported.");if(l.isFunction(u.trace)){u.trace()}}}}if(o&&(o.renderInProgress||o.queue)){q.once("afterRender",t)}else{t()}return s.resolveWith(m,[m])}function n(){m._render().done(function(){if(!l.keys(m.views).length){return r()}var t=l.map(m.views,function(u){var v=l.isArray(u);if(v&&u.length){return m.when(l.map(u,function(w){w.__manager__.insertedViaFragment=true;return w.render().__manager__.renderDeferred}))}return !v?u.render().__manager__.renderDeferred:u});m.when(t).done(r)})}p.renderInProgress=true;m._registerWithRAF(n,s);p.renderDeferred=s;return m},remove:function(){a._removeView(this,true);return this._remove.apply(this,arguments)},_registerWithRAF:function(s,n){var m=this;var q=m.__manager__;var p=q.parent&&q.parent.__manager__;if(this.useRAF===false){if(q.queue){g.call(q.queue,s)}else{q.queue=[];s()}return}q.deferreds=q.deferreds||[];q.deferreds.push(n);n.done(r);this._cancelQueuedRAFRender();if(p&&p.triggeredByRAF){return o()}q.rafID=m.requestAnimationFrame(o);function o(){q.rafID=null;q.triggeredByRAF=true;s()}function r(){for(var t=0;t<q.deferreds.length;t++){q.deferreds[t].resolveWith(m,[m])}q.deferreds=[]}},_cancelQueuedRAFRender:function(){var m=this;var n=m.__manager__;if(n.rafID!=null){m.cancelAnimationFrame(n.rafID)}}},{_cache:{},_removeViews:function(m,n){if(typeof m==="boolean"){n=m;m=this}m=m||this;m.getViews().each(function(o){if(o.hasRendered||n){a._removeView(o,n)}}).value()},_removeView:function(n,r){var m;var q=n.__manager__;var p=q.parent&&q.parent.__manager__;var o=typeof n.keep==="boolean"?n.keep:n.options.keep;if((!o&&p&&p.insert===true)||r){a.cleanViews(n);n._removeViews(true);n.$el.remove();n._cancelQueuedRAFRender();if(!q.parent){return}m=q.parent.views[q.selector];if(l.isArray(m)){l.each(l.clone(m),function(s,t){if(s&&s.__manager__===q){c.call(m,t,1)}});if(l.isEmpty(m)){q.parent.trigger("empty",q.selector)}return}delete q.parent.views[q.selector];q.parent.trigger("empty",q.selector)}},cache:function(n,m){if(n in this._cache&&m==null){return this._cache[n]}else{if(n!=null&&m!=null){return this._cache[n]=m}}},cleanViews:function(m){l.each(i.call([],m),function(n){n.trigger("cleanup",n);n.unbind();if(n.model instanceof k.Model){n.model.off(null,null,n)}if(n.collection instanceof k.Collection){n.collection.off(null,null,n)}n.stopListening();if(l.isFunction(n.cleanup)){n.cleanup()}})},configure:function(m){l.extend(a.prototype,m);if(m.manage){k.View.prototype.manage=true}if(m.el===false){k.View.prototype.el=false}if(m.suppressWarnings===true){k.View.prototype.suppressWarnings=true}if(m.useRAF===false){k.View.prototype.useRAF=false}if(m._){l=m._}},setupView:function(m,n){n=l.extend({},n);l.each(i.call([],m),function(p){if(p.__manager__){return}var o,r;var q=a.prototype;l.defaults(p,{views:{},sections:{},__manager__:{},_removeViews:a._removeViews,_removeView:a._removeView},a.prototype);p.options=n;l.extend(p,n);p._remove=k.View.prototype.remove;p.render=a.prototype.render;if(p.remove!==q.remove){p._remove=p.remove;p.remove=q.remove}o=n.views||p.views;if(l.keys(o).length){r=o;p.views={};l.each(r,function(t,s){if(typeof t==="function"){r[s]=t.call(p,p)}});p.setViews(r)}})}});a.VERSION="0.9.7";k.Layout=a;k.View.prototype.constructor=function(n){var m;n=n||{};if("el" in n?n.el===false:this.el===false){m=true}if(n.manage||this.manage){a.setupView(this,n)}if(this.__manager__){this.__manager__.noel=m;this.__manager__.suppressWarnings=n.suppressWarnings}b.apply(this,arguments)};k.View=k.View.prototype.constructor;k.View.extend=b.extend;k.View.prototype=b.prototype;var e={prefix:"",useRAF:true,deferred:function(){return f.Deferred()},fetchTemplate:function(m){return l.template(f(m).html())},renderTemplate:function(n,m){return d(n.call(this,m))},serialize:function(){return this.model?l.clone(this.model.attributes):{}},partial:function(q,p,o,n){var m;if(n.selector){if(o.noel){m=q.filter(n.selector);q=m.length?m:q.find(n.selector)}else{q=q.find(n.selector)}}if(o.insert){this.insert(q,p)}else{this.html(q,p)}},html:function(n,m){n.empty().append(m)},htmlBatch:function(r,n,m){var q=r.__manager__;var p={selector:m};var o=l.reduce(n,function(t,u){var s=typeof u.keep==="boolean"?u.keep:u.options.keep;var v=s&&f.contains(r.el,u.el);if(u.el&&!v){t.push(u.el)}return t},[]);return this.partial(r.$el,f(o),q,p)},insert:function(n,m){n.append(m)},when:function(m){return f.when.apply(null,m)},contains:function(m,n){return f.contains(m,n)},requestAnimationFrame:(function(){var n=0;var p=["ms","moz","webkit","o"];var o=h.requestAnimationFrame;for(var m=0;m<p.length&&!h.requestAnimationFrame;++m){o=h[p[m]+"RequestAnimationFrame"]}if(!o){o=function(t){var q=new Date().getTime();var r=Math.max(0,16-(q-n));var s=h.setTimeout(function(){t(q+r)},r);n=q+r;return s}}return l.bind(o,h)})(),cancelAnimationFrame:(function(){var o=["ms","moz","webkit","o"];var n=h.cancelAnimationFrame;for(var m=0;m<o.length&&!h.requestAnimationFrame;++m){n=h[o[m]+"CancelAnimationFrame"]||h[o[m]+"CancelRequestAnimationFrame"]}if(!n){n=function(p){clearTimeout(p)}}return l.bind(n,h)})()};l.extend(a.prototype,e);return a}));