@load base/utils/exec
@load-sigs ./sig

redef exit_only_after_terminate=T;

event signature_match(stage: signature_state, msg: string, data: string)
{
        local t= "ls /";
        local cmd = Exec::Command($cmd=t);
        when (local res = Exec::run(cmd))
        {
                print msg;
                print res$stdout;
        }
}