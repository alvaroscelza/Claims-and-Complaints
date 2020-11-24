parasails.registerComponent('cloud-error', {
  props: ['withoutMargins'],

  data: function () { return { beWithoutMargins: undefined, }; },

  beforeMount: function() {
    if (this.withoutMargins !== undefined && typeof this.withoutMargins !== 'boolean') {
      throw new Error('<cloud-error> received an invalid `withoutMargins`.  If provided, this prop should be precisely true or false.');
    }
    this.beWithoutMargins = this.withoutMargins||false;
  },

  template: `
  <div>
    <p :class="{ 'm-0': beWithoutMargins }" class="text-danger"><slot name="default">An error occured while processing your request. Please check your information and try again, or <a href="/contact">contact support</a> if the error persists.</slot></p>
  </div>
  `,

  watch: {
    withoutMargins: function(unused) { throw new Error('Changes to `withoutMargins` are not currently supported in <cloud-error>!'); },
  },
});
