# -*- coding: utf-8 -*-

# Import Salt Testing libs
from salttesting import skipIf, TestCase
from salttesting.helpers import ensure_in_syspath
from salttesting.mock import NO_MOCK, NO_MOCK_REASON, MagicMock
ensure_in_syspath('../../')

# Import salt libs
from salt.modules import linux_acl
from salt.exceptions import CommandExecutionError


@skipIf(NO_MOCK, NO_MOCK_REASON)
class LinuxAclTestCase(TestCase):

    def setUp(self):
        linux_acl.__salt__ = {'cmd.run': MagicMock()}
        self.cmdrun = linux_acl.__salt__['cmd.run']
        self.file = '/tmp/file'
        self.files = ['/tmp/file1', '/tmp/file2']
        self.u_acl = ['u', 'myuser', 'rwx']
        self.user_acl = ['user', 'myuser', 'rwx']
        self.user_acl_cmd = 'u:myuser:rwx'
        self.g_acl = ['g', 'mygroup', 'rwx']
        self.group_acl = ['group', 'mygroup', 'rwx']
        self.group_acl_cmd = 'g:mygroup:rwx'
        self.d_u_acl = ['d:u', 'myuser', 'rwx']
        self.d_user_acl = ['d:user', 'myuser', 'rwx']
        self.default_user_acl = ['d:user', 'myuser', 'rwx']
        self.default_user_acl_cmd = 'd:u:myuser:rwx'

    # too easy to test (DRY)
    def test_version(self):
        pass

    def test_getfacl_wo_args(self):
        self.assertRaises(CommandExecutionError, linux_acl.getfacl)

    def test_getfacl_w_single_arg(self):
        linux_acl.getfacl(self.file)
        self.cmdrun.assert_called_once_with('getfacl -p ' + self.file)

    def test_getfacl_w_multiple_args(self):
        linux_acl.getfacl(*self.files)
        self.cmdrun.assert_called_once_with('getfacl -p ' + ' '.join(self.files))

    def test_getfacl__recursive_w_multiple_args(self):
        linux_acl.getfacl(*self.files, recursive=True)
        self.cmdrun.assert_called_once_with('getfacl -p -R ' + ' '.join(self.files))

    def test_wipefacls_wo_args(self):
        self.assertRaises(CommandExecutionError, linux_acl.wipefacls)

    def test_wipefacls_w_single_arg(self):
        linux_acl.wipefacls(self.file)
        self.cmdrun.assert_called_once_with('setfacl -b ' + self.file)

    def test_wipefacls_w_multiple_args(self):
        linux_acl.wipefacls(*self.files)
        self.cmdrun.assert_called_once_with('setfacl -b ' + ' '.join(self.files))

    def test_wipefacls__recursive_w_multiple_args(self):
        linux_acl.wipefacls(*self.files, recursive=True)
        self.cmdrun.assert_called_once_with('setfacl -b -R ' + ' '.join(self.files))

    def test_modfacl_wo_args(self):
        for acl in [self.u_acl, self.user_acl, self.g_acl, self.group_acl]:
            self.assertRaises(CommandExecutionError, linux_acl.modfacl, *acl)

    def test_modfacl__u_w_single_arg(self):
        linux_acl.modfacl(*(self.u_acl + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.user_acl_cmd, self.file]))

    def test_modfacl__u_w_multiple_args(self):
        linux_acl.modfacl(*(self.u_acl + self.files))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.user_acl_cmd] + self.files))

    def test_modfacl__user_w_single_arg(self):
        linux_acl.modfacl(*(self.user_acl + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.user_acl_cmd, self.file]))

    def test_modfacl__user_w_multiple_args(self):
        linux_acl.modfacl(*(self.user_acl + self.files))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.user_acl_cmd] + self.files))

    def test_modfacl__g_w_single_arg(self):
        linux_acl.modfacl(*(self.g_acl + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.group_acl_cmd, self.file]))

    def test_modfacl__g_w_multiple_args(self):
        linux_acl.modfacl(*(self.g_acl + self.files))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.group_acl_cmd] + self.files))

    def test_modfacl__group_w_single_arg(self):
        linux_acl.modfacl(*(self.group_acl + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.group_acl_cmd, self.file]))

    def test_modfacl__group_w_multiple_args(self):
        linux_acl.modfacl(*(self.group_acl + self.files))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.group_acl_cmd] + self.files))

    def test_modfacl__d_u_w_single_arg(self):
        linux_acl.modfacl(*(self.d_u_acl + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.default_user_acl_cmd, self.file]))

    def test_modfacl__d_u_w_multiple_args(self):
        linux_acl.modfacl(*(self.d_u_acl + self.files))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.default_user_acl_cmd] + self.files))

    def test_modfacl__d_user_w_single_arg(self):
        linux_acl.modfacl(*(self.d_user_acl + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.default_user_acl_cmd, self.file]))

    def test_modfacl__d_user_w_multiple_args(self):
        linux_acl.modfacl(*(self.d_user_acl + self.files))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.default_user_acl_cmd] + self.files))

    def test_modfacl__default_user_w_single_arg(self):
        linux_acl.modfacl(*(self.default_user_acl + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.default_user_acl_cmd, self.file]))

    def test_modfacl__default_user_w_multiple_args(self):
        linux_acl.modfacl(*(self.default_user_acl + self.files))
        self.cmdrun.assert_called_once_with('setfacl -m ' + ' '.join([self.default_user_acl_cmd] + self.files))

    def test_modfacl__recursive_w_multiple_args(self):
        linux_acl.modfacl(*(self.user_acl + self.files), recursive=True)
        self.cmdrun.assert_called_once_with('setfacl -m -R ' + ' '.join([self.user_acl_cmd] + self.files))

    def test_delfacl_wo_args(self):
        for acl in [self.u_acl, self.user_acl, self.g_acl, self.group_acl]:
            self.assertRaises(CommandExecutionError, linux_acl.delfacl, *acl[:-1])

    def test_delfacl__u_w_single_arg(self):
        linux_acl.delfacl(*(self.u_acl[:-1] + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.user_acl_cmd.rpartition(':')[0], self.file]))

    def test_delfacl__u_w_multiple_args(self):
        linux_acl.delfacl(*(self.u_acl[:-1] + self.files))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.user_acl_cmd.rpartition(':')[0]] + self.files))

    def test_delfacl__user_w_single_arg(self):
        linux_acl.delfacl(*(self.user_acl[:-1] + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.user_acl_cmd.rpartition(':')[0], self.file]))

    def test_delfacl__user_w_multiple_args(self):
        linux_acl.delfacl(*(self.user_acl[:-1] + self.files))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.user_acl_cmd.rpartition(':')[0]] + self.files))

    def test_delfacl__g_w_single_arg(self):
        linux_acl.delfacl(*(self.g_acl[:-1] + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.group_acl_cmd.rpartition(':')[0], self.file]))

    def test_delfacl__g_w_multiple_args(self):
        linux_acl.delfacl(*(self.g_acl[:-1] + self.files))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.group_acl_cmd.rpartition(':')[0]] + self.files))

    def test_delfacl__group_w_single_arg(self):
        linux_acl.delfacl(*(self.group_acl[:-1] + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.group_acl_cmd.rpartition(':')[0], self.file]))

    def test_delfacl__group_w_multiple_args(self):
        linux_acl.delfacl(*(self.group_acl[:-1] + self.files))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.group_acl_cmd.rpartition(':')[0]] + self.files))

    def test_delfacl__d_u_w_single_arg(self):
        linux_acl.delfacl(*(self.d_u_acl[:-1] + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.default_user_acl_cmd.rpartition(':')[0], self.file]))

    def test_delfacl__d_u_w_multiple_args(self):
        linux_acl.delfacl(*(self.d_u_acl[:-1] + self.files))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.default_user_acl_cmd.rpartition(':')[0]] + self.files))

    def test_delfacl__d_user_w_single_arg(self):
        linux_acl.delfacl(*(self.d_user_acl[:-1] + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.default_user_acl_cmd.rpartition(':')[0], self.file]))

    def test_delfacl__d_user_w_multiple_args(self):
        linux_acl.delfacl(*(self.d_user_acl[:-1] + self.files))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.default_user_acl_cmd.rpartition(':')[0]] + self.files))

    def test_delfacl__default_user_w_single_arg(self):
        linux_acl.delfacl(*(self.default_user_acl[:-1] + [self.file]))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.default_user_acl_cmd.rpartition(':')[0], self.file]))

    def test_delfacl__default_user_w_multiple_args(self):
        linux_acl.delfacl(*(self.default_user_acl[:-1] + self.files))
        self.cmdrun.assert_called_once_with('setfacl -x ' + ' '.join([self.default_user_acl_cmd.rpartition(':')[0]] + self.files))

    def test_delfacl__recursive_w_multiple_args(self):
        linux_acl.delfacl(*(self.default_user_acl[:-1] + self.files), recursive=True)
        self.cmdrun.assert_called_once_with('setfacl -x -R ' + ' '.join([self.default_user_acl_cmd.rpartition(':')[0]] + self.files))
