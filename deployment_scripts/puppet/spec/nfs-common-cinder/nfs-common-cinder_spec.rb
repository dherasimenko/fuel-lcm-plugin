require 'spec_helper'

# check if cinder-volume installed
describe package('cinder-volume'), :if => os[:family] == 'ubuntu' do
  it { should be_installed }
end

describe package('nfs-common'), :if => os[:family] == 'ubuntu' do
  it { should be_installed }
end

describe service('cinder-volume'), :if => os[:family] == 'ubuntu' do
  it { should be_enabled }
  it { should be_running }
end

# check if cinder config exist
describe file('/etc/cinder/cinder.conf'), :if => os[:family] == 'ubuntu' do
  it { should be_file }
  it { should be_owned_by 'cinder' }
  it { should be_grouped_into 'cinder' }
end

# check if cinder have all needed config changes
describe file('/etc/cinder/cinder.conf') do
  it { should contain 'volume_driver=cinder.volume.drivers.nfs.NfsDriver' }
  it { should contain 'nfs_shares_config'}
  it { should contain 'nfs_sparsed_volumes'}
  it { should contain 'nfs_oversub_ratio'}
  it { should contain 'nfs_used_ratio'}
  it { should contain 'nfs_mount_attempts'}
  it { should contain 'nfs_mount_point_base'}
end

# check if nfs mapping for cinder exist
describe file('/etc/cinder/nfs_shares.txt'), :if => os[:family] == 'ubuntu' do
  it { should be_file }
end
