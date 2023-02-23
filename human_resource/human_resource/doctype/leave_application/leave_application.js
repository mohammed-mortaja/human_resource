// Copyright (c) 2023, moh and contributors
// For license information, please see license.txt


frappe.ui.form.on("Leave Application", {
  from_date: function (frm) {
    frm.trigger("leave_balance_");
    frm.trigger("total_leave_days_");
  },
  to_date: function (frm) {
    frm.trigger("leave_balance_");
    frm.trigger("total_leave_days_");
  },
  leave_type: function (frm) {
    frm.trigger("leave_balance_");
  },
  employee: function (frm) {
    frm.trigger("leave_balance_");
  },

  get_total_leaves_before_application: function (frm) {
    if (
      frm.doc.leave_type != undefined &&
      frm.doc.employee != undefined &&
      frm.doc.from_date != undefined &&
      frm.doc.to_date != undefined
    ) {
      frappe.call({
        method:
          "human_resource.human_resource.doctype.leave_application.leave_application.get_total_leaves",
        args: {
          employee: frm.doc.employee,
          leave_type: frm.doc.leave_type,
          from_date: frm.doc.from_date,
          to_date: frm.doc.to_date,
        },

        callback: (r) => {
          frm.doc.leave_balance_before_application = r.message;
          frm.refresh();
        },
      });
    }
  },

  get_total_leave_days: function (frm) {
    if (frm.doc.from_date != undefined && frm.doc.to_date != undefined) {
      frappe.call({
        method:
          "human_resource.human_resource.doctype.leave_application.leave_application.get_total_leave_days",
        args: {
          from_date: frm.doc.from_date,
          to_date: frm.doc.to_date,
        },

        callback: (r) => {
          frm.doc.total_leave_days = r.message;
          frm.refresh();
        },
      });
    }
  },
});

